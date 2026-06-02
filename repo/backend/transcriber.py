import os
import torch
import whisper
from pyannote.audio import Pipeline
from dotenv import load_dotenv

load_dotenv()


class Transcriber:
    def __init__(self, model_size='base'):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.whisper_model = whisper.load_model(model_size, device=self.device)
        self.pyannote_pipeline = None
        self._init_pyannote()

    def _init_pyannote(self):
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        if hf_token:
            try:
                self.pyannote_pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=hf_token
                )
            except Exception as e:
                print(f"Warning: Could not load pyannote pipeline: {e}")
                self.pyannote_pipeline = None

    def diarize_speakers(self, audio_path):
        if self.pyannote_pipeline is None:
            return self._fallback_diarization(audio_path)

        diarization = self.pyannote_pipeline(audio_path)
        segments = []

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                'start': turn.start,
                'end': turn.end,
                'speaker': speaker
            })

        return segments

    def _fallback_diarization(self, audio_path):
        import librosa
        y, sr = librosa.load(audio_path)
        duration = librosa.get_duration(y=y, sr=sr)

        return [{
            'start': 0,
            'end': duration,
            'speaker': 'SPEAKER_00'
        }]

    def extract_teacher_segments(self, diarization, teacher_name):
        if not diarization:
            return []

        speaker_counts = {}
        for seg in diarization:
            speaker = seg['speaker']
            speaker_counts[speaker] = speaker_counts.get(speaker, 0) + (seg['end'] - seg['start'])

        if teacher_name and teacher_name in speaker_counts:
            teacher_speaker = teacher_name
        else:
            teacher_speaker = max(speaker_counts, key=speaker_counts.get)

        teacher_segments = [
            seg for seg in diarization if seg['speaker'] == teacher_speaker
        ]

        return self._merge_segments(teacher_segments)

    def _merge_segments(self, segments, gap_threshold=1.0):
        if not segments:
            return []

        merged = []
        current = segments[0].copy()

        for seg in segments[1:]:
            if seg['start'] - current['end'] < gap_threshold:
                current['end'] = seg['end']
            else:
                merged.append(current)
                current = seg.copy()

        merged.append(current)
        return merged

    def transcribe_segments(self, audio_path, segments):
        if not segments:
            full_result = self.whisper_model.transcribe(
                audio_path,
                language='zh',
                verbose=False
            )
            return self._format_transcription(full_result['segments'])

        all_transcriptions = []

        for seg in segments:
            result = self.whisper_model.transcribe(
                audio_path,
                language='zh',
                verbose=False,
                initial_prompt="这是一个手工皮具制作教学的音频，包含皮革知识、工具使用技巧和缝线步骤讲解。"
            )

            for t_segment in result['segments']:
                t_start = t_segment['start'] + seg['start']
                t_end = t_segment['end'] + seg['start']

                if t_start >= seg['start'] and t_end <= seg['end']:
                    all_transcriptions.append({
                        'start': t_start,
                        'end': t_end,
                        'text': t_segment['text'],
                        'speaker': '老师'
                    })

        all_transcriptions.sort(key=lambda x: x['start'])
        return all_transcriptions

    def _format_transcription(self, segments):
        formatted = []
        for seg in segments:
            formatted.append({
                'start': seg['start'],
                'end': seg['end'],
                'text': seg['text'],
                'speaker': '老师'
            })
        return formatted
