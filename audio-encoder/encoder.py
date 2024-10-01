import numpy as np
from scipy.io.wavfile import write

# Parameters
sample_rate = 8000  # 44.1 kHz sample rate bit i have tried to reduce it to reduce the space of code
duration = 1  # Duration of each frequency (in seconds)

# Frequency ranges for each character
char_freq_map = {
    '0': (1000, 1050), '1': (1050, 1100), '2': (1100, 1150), '3': (1150, 1200),
    '4': (1200, 1250), '5': (1250, 1300), '6': (1300, 1350), '7': (1350, 1400),
    '8': (1400, 1450), '9': (1450, 1500), 'a': (1500, 1550), 'b': (1550, 1600),
    'c': (1600, 1650), 'd': (1650, 1700), 'e': (1700, 1750), 'f': (1750, 1800)
}


def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * 2 * np.pi * t)
    return tone

def encode_sha256_to_audio(sha_string, sample_rate, duration):
    audio_signal = np.array([])

    for char in sha_string:
        if char in char_freq_map:
            freq_range = char_freq_map[char]
            frequency = np.random.uniform(*freq_range)  # a random frequency within the range p.s. agr random nai rkhna ho toh bata dena
            tone = generate_sine_wave(frequency, duration, sample_rate)
            audio_signal = np.concatenate((audio_signal, tone))

    return audio_signal

# Example usage
sha256_string = 'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'  # SHA string
audio_signal = encode_sha256_to_audio(sha256_string, sample_rate, duration)

# Normalize to 16-bit PCM format
audio_signal = np.int16(audio_signal / np.max(np.abs(audio_signal)) * 32767)

# Save to WAV file
write("encoded_sha256_audio.wav", sample_rate, audio_signal)
