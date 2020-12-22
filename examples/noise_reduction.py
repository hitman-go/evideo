from scipy.io import wavfile
import numpy as np
import noisereduce as nr
from pydub import AudioSegment

#sound = AudioSegment.from_wav("sample.wav")
#sound = sound.set_channels(1)
#sound.export("sample_1.wav", format="wav")
rate, origin_data = wavfile.read("sample_1.wav")
data = origin_data[:rate*30]
ave_value = np.average(abs(data))
low_data = np.array([d for d in data if np.average(abs(d)) < ave_value])
noise_th = np.average(abs(low_data))
noise_data = np.array([d for d in data if np.average(abs(d)) < noise_th])
reduced_noise = nr.reduce_noise(audio_clip=origin_data.astype(np.float),
                                noise_clip=noise_data.astype(np.float), verbose=True)
wavfile.write('sample_reduce_noise.wav', rate, reduced_noise.astype(np.int16))
