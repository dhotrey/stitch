import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft

# Frequency ranges for each character
char_freq_map = {
    '0': (1000, 1050), '1': (1050, 1100), '2': (1100, 1150), '3': (1150, 1200),
    '4': (1200, 1250), '5': (1250, 1300), '6': (1300, 1350), '7': (1350, 1400),
    '8': (1400, 1450), '9': (1450, 1500), 'a': (1500, 1550), 'b': (1550, 1600),
    'c': (1600, 1650), 'd': (1650, 1700), 'e': (1700, 1750), 'f': (1750, 1800)
}

def decode_audio_to_sha256(filename, sample_rate, duration):
    # Read the WAV file
    sr, audio_signal = read(filename)

    if sr != sample_rate:
        raise ValueError(f"Sample rate of file ({sr}) does not match the expected rate ({sample_rate}).")

    # Calculate number of samples per character (since each tone has a fixed duration of 1 second)
    samples_per_char = int(sample_rate * duration)
    
    # Initialize an empty string for the decoded SHA-256 hash
    decoded_sha256 = ""

    for i in range(0, len(audio_signal), samples_per_char):
        segment = audio_signal[i:i+samples_per_char]

      
        spectrum = np.abs(fft(segment))[:len(segment)//2]
        freqs = np.fft.fftfreq(len(segment), 1/sample_rate)[:len(segment)//2]

       
        dominant_freq = freqs[np.argmax(spectrum)]


        for char, (low, high) in char_freq_map.items():
            if low <= dominant_freq <= high:
                decoded_sha256 += char
                break

    return decoded_sha256

filename = "encoded_sha256_audio.wav"  
sample_rate = 8000  # Must match the sample rate used during encoding
duration = 1  # Duration of each character's tone (in seconds)

# Decode the audio back to the SHA-256 string
decoded_sha256 = decode_audio_to_sha256(filename, sample_rate, duration)
print(f"Decoded SHA-256 string: {decoded_sha256}")
