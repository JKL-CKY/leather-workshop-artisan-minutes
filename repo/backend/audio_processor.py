import librosa
import numpy as np
import soundfile as sf
import tempfile
import os


class AudioProcessor:
    def __init__(self, sr=22050):
        self.sr = sr

    def remove_tapping_noise(self, audio_path):
        y, sr = librosa.load(audio_path, sr=self.sr)

        D = librosa.stft(y)
        S_full, phase = librosa.magphase(D)

        S_filter = librosa.decompose.nn_filter(
            S_full,
            aggregate=np.median,
            metric='cosine',
            width=int(librosa.time_to_frames(0.05, sr=sr))
        )

        S_filter = np.minimum(S_full, S_filter)

        margin_i, margin_v = 3, 10
        power = 2

        mask_i = librosa.util.softmask(
            S_filter,
            margin_i * (S_full - S_filter),
            power=power
        )

        mask_v = librosa.util.softmask(
            S_full - S_filter,
            margin_v * S_filter,
            power=power
        )

        S_foreground = mask_v * S_full
        S_background = mask_i * S_full

        y_foreground = librosa.istft(S_foreground * phase)

        D_harmonic, D_percussive = librosa.decompose.hpss(S_foreground)
        y_harmonic = librosa.istft(D_harmonic * phase)

        y_denoised = self._spectral_subtraction(y_harmonic, sr)
        y_denoised = self._adaptive_threshold(y_denoised, sr)

        fd, cleaned_path = tempfile.mkstemp(suffix='.wav')
        os.close(fd)
        sf.write(cleaned_path, y_denoised, sr)

        return cleaned_path

    def _spectral_subtraction(self, y, sr, noise_reduce=0.5):
        D = librosa.stft(y)
        mag, phase = librosa.magphase(D)

        noise_est = np.mean(mag[:, :int(sr * 0.5)], axis=1, keepdims=True)
        mag_clean = np.maximum(mag - noise_reduce * noise_est, 0)

        y_clean = librosa.istft(mag_clean * phase)
        return y_clean

    def _adaptive_threshold(self, y, sr, threshold_factor=1.5):
        energy = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        energy_thresh = np.mean(energy) * threshold_factor

        frames = librosa.util.frame(y, frame_length=2048, hop_length=512)
        for i in range(len(energy)):
            if energy[i] > energy_thresh:
                frames[:, i] *= 0.3

        y_processed = librosa.util.frame(frames, frame_length=2048, hop_length=512, axis=1)
        return y
