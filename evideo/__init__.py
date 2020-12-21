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

from .base import Video
from .audio import Audio
import os
import shutil


def amplify_sound(input_file, output_file, set_video_flag=True):
    ext_ = os.path.splitext(os.path.basename(input_file))[1]
    if ext_ == ".mp4":
        if set_video_flag:
            if os.path.exists(output_file):
                os.remove(output_file)
            shutil.copy2(input_file, output_file)
        # get mp3 from mp4
        mp3_file = os.path.splitext(os.path.basename(input_file))[0] + ".mp3"
        video_ = Video(input_file)
        video_.get_mp3(mp3_file, input_file)
    else:
        if os.path.exists(output_file):
            os.remove(output_file)
            shutil.copy2(input_file, output_file)
            mp3_file = output_file
    # amplify mp3 file
    audio_ = Audio(mp3_file)
    audio_.amplify()

    # set mp3 to mp4
    if set_video_flag and ext_ == ".mp4":
        video_.set_mp3(mp3_file, output_file)
