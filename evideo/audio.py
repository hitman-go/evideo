from pydub import AudioSegment
import pydub


class Audio:
    def __init__(self, input_audio):
        self.input_audio = input_audio
        self.base_sound = AudioSegment.from_file(input_audio, format="mp3")

    def amplify(self, target_dBFS=-20):
        """According to my own research, the best dBFS for Youtube is -20"""
        change_in_dBFS = target_dBFS - self.base_sound.dBFS
        amp_sound = self.base_sound.apply_gain(change_in_dBFS)
        amp_sound.export(self.input_audio, format="mp3")
