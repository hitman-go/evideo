from pydub import AudioSegment
import pydub

class Audio:
    def __init__(self, input_audio):
        self.input_audio = input_audio
        base_sound = AudioSegment.from_file(input_audio, format="mp3")
        print(base_sound.rms)
