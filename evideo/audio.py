# MIT License
#
# Copyright (c) 2020 hitman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pydub import AudioSegment
import pydub


class Audio:
    def __init__(self, input_audio, audio_format="wav"):
        self.input_audio = input_audio
        self.base_sound = AudioSegment.from_file(
            input_audio, format=audio_format)
        self.audio_format = audio_format

    def amplify(self, target_dBFS=-20):
        """According to my own research, the best dBFS for Youtube is -20"""
        change_in_dBFS = target_dBFS - self.base_sound.dBFS
        amp_sound = self.base_sound.apply_gain(change_in_dBFS)
        amp_sound.export(self.input_audio, format=self.audio_format)
