import subprocess
import time
from typing import List, Union, Tuple, Optional
from dataclasses import dataclass

import numpy as np
import torch
from torch.nn.functional import pad

import whisper
from whisper.audio import (
    SAMPLE_RATE, N_FRAMES, HOP_LENGTH, N_SAMPLES, N_SAMPLES_PER_TOKEN, TOKENS_PER_SECOND, FRAMES_PER_SECOND, N_FFT,
    pad_or_trim, log_mel_spectrogram
)
from whisper.decoding import DecodingOptions

from .audio import AudioLoader
from .utils import isolate_useful_options
from .whisper_compatibility import get_tokenizer
from .decode import decode_stable
from .timing import _split_tokens, add_word_timestamps_stable
from .result import WhisperResult


@dataclass
class TempWord:
    word_dict: dict
    offset: Optional[float] = None

    def __post_init__(self):
        self.match = 0

    @property
    def start(self) -> float:
        return self.word_dict['start']

    @property
    def end(self) -> float:
        return self.word_dict['end']

    @property
    def word(self) -> str:
        return self.word_dict['word']

    @property
    def probability(self) -> float:
        return self.word_dict['probability']

    @property
    def tokens(self) -> List[int]:
        return self.word_dict['tokens']

    @start.setter
    def start(self, new_start: float):
        self.word_dict['start'] = new_start

    @end.setter
    def end(self, new_end: float):
        self.word_dict['end'] = new_end

    def update_word(self, new_word: "TempWord", update_ts: bool = False):
        if update_ts:
            self.word_dict = new_word.word_dict
            return
        self.word_dict['word'] = new_word.word
        self.word_dict['probability'] = new_word.probability
        self.word_dict['tokens'] = new_word.tokens

    def is_text_match(self, other_word: "TempWord") -> bool:
        text = self.normalize_word()
        other_text = other_word.normalize_word()
        return text == other_text[:len(text)] or text[-len(other_text):] == other_text

    def normalize_word(self) -> str:
        return self.word.strip().strip(',').strip('.').strip('!').lower()


def transcribe_live(
        model: whisper.Whisper,
        audio,
        chunk_length: Union[int, str] = '0.25s',
        language: str = 'en',
        no_speech_threshold: float = 0.6,
        k=2,
        **kwargs
):
    if isinstance(chunk_length, str):
        assert chunk_length.endswith('s')
        chunk_length = round(float(chunk_length[:-1]) * SAMPLE_RATE)
    if not isinstance(audio, AudioLoader):
        audio = AudioLoader(audio, chunk_length, sr=SAMPLE_RATE)
    dtype = torch.float16
    assert not isinstance(kwargs.get('temperature'), (list, tuple)), 'temperature can only be a single value'
    task = 'transcribe'
    tokenizer = get_tokenizer(model, language=language, task=task)
    start_time = time.time()
    temp_words: List[TempWord] = []
    all_words: List[TempWord] = []
    seek = 0
    total_accum_samples = 0
    prev_chunk_length = 0

    def timestamp_words(_words, _tokens) -> List[TempWord]:
        mel = mel_chunk
        # mel = log_mel_spectrogram(
        #     pad(audio_chunk, (0, mel_pad)),
        #     n_mels
        # ).to(device=model.device, dtype=dtype)
        # mel = pad_or_trim(mel, N_FRAMES)

        offset = round(seek/SAMPLE_RATE, 3)
        temp_segment = dict(
            seek=offset,
            tokens=(_words, _tokens)
        )

        add_word_timestamps_stable(
            segments=[temp_segment],
            model=model,
            tokenizer=tokenizer,
            mel=mel,
            audio_features=audio_feature,
            num_samples=curr_chunk_length,
            split_callback=(lambda x, _: x),
            gap_padding=None
        )

        return [TempWord(w, offset=offset) for w in temp_segment['words']]

    n_mels = model.dims.n_mels
    n_samples = N_SAMPLES

    mel_pad = N_FFT // 2

    prefix_cutoff_idx = 0

    while True:
        if prefix_cutoff_idx < len(all_words):
            prefix = all_words[prefix_cutoff_idx:][-4:]
            prefix_words_len = len(prefix)
            new_seek = round(prefix[0].start * SAMPLE_RATE)
            assert new_seek >= seek, f'{prefix[0].start} {seek / SAMPLE_RATE}'
            prev_chunk_length += (seek - new_seek)
            seek = new_seek
            kwargs['prefix'] = [t for w in prefix for t in w.tokens]
        else:
            prefix_words_len = 0
            kwargs['prefix'] = None

        audio_chunk = audio.next_chunk(seek, prev_chunk_length+chunk_length)
        if audio_chunk is None:
            break
        curr_chunk_length = audio_chunk.shape[-1]

        left_pad = N_SAMPLES - curr_chunk_length
        assert left_pad >= 0
        mel_chunk = log_mel_spectrogram(
            pad(audio_chunk, (0, left_pad)),
            n_mels
        ).to(device=model.device, dtype=dtype)
        # prefix = [t for w in prefix_words for t in w['tokens']]
        decoding_options = DecodingOptions(**kwargs, without_timestamps=True, language=language)
        result, audio_feature = decode_stable(model, mel_chunk, decoding_options)

        # non-speech
        if result.no_speech_prob > no_speech_threshold or not result.tokens:
            temp_words = []
            prev_chunk_length = 0
            seek += curr_chunk_length
            prefix_cutoff_idx = len(all_words)
            continue

        prefix = kwargs['prefix'] or []
        words = timestamp_words(*_split_tokens(prefix+result.tokens, tokenizer))[prefix_words_len:]
        if all_words and all_words[-1].end > words[0].start:
            min_offset = all_words[-1].end
            for w in words:
                if w.start >= min_offset:
                    break
                w.start = min_offset
                if w.end >= min_offset:
                    break
                w.end = min_offset
        if all_words and words[0].is_text_match(all_words[-1]):
            if len(words) == 1:
                temp_words = []
                prev_chunk_length = 0
                seek += curr_chunk_length
                prefix_cutoff_idx = len(all_words)
                continue
            del words[0]

        last_i = None
        # match_count = 0
        if len(temp_words) > len(words):
            temp_words = temp_words[:len(words)]

        for i, word in enumerate(words):
            if i < len(temp_words):
                prev_word = temp_words[i]
                is_match = prev_word.is_text_match(word)
                if not is_match and (i == 0 or (i+1) == len(words)) and prev_word.probability >= word.probability:
                    is_match = True
                    word.update_word(prev_word)

                if is_match:
                    # match_count += 1
                    if i == 0 or (i+1) != len(words):
                        prev_word.update_word(word, True)
                    prev_word.match += 1
                    if prev_word.match > k:
                        if all_words and word.word == all_words[-1].word:
                            print('T')
                        print(word.word)
                        last_i = i + 1
                else:
                    prev_word.update_word(word, True)
            else:
                temp_words.append(word)

        if last_i is None:
            prev_chunk_length = curr_chunk_length
        else:
            new_words, temp_words = temp_words[:last_i], temp_words[last_i:]
            all_words.extend(new_words)
            prev_chunk_length = curr_chunk_length

    audio.terminate()
    result = WhisperResult([[w.word_dict for w in all_words]])
    return result


