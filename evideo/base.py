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

import cv2
from cv2 import CAP_PROP_FRAME_COUNT
from tqdm import tqdm
import os
import ffmpeg
import shutil
from pydub import AudioSegment


class Video:
    def __init__(self, input_video, output_video=None):
        self.input_video = input_video
        self.output_video = output_video
        self.cap = cv2.VideoCapture(input_video)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        if output_video is not None:
            self.writer = cv2.VideoWriter(
                output_video, fourcc, self.fps, (self.width, self.height))
        opencv_face_xml = "haarcascade_frontalface_default.xml"
        if os.path.exists(opencv_face_xml):
            self.cascade = cv2.CascadeClassifier(opencv_face_xml)

    def __del__(self):
        try:
            self.writer.release()
        except BaseException:
            pass
        self.cap.release()
        cv2.destroyAllWindows()

    def get_sound(self, audio_name, input_video=None):
        """get sound from mp4"""
        if input_video is None:
            input_video = self.input_video
        stream = ffmpeg.input(input_video)
        stream = ffmpeg.output(
            stream,
            audio_name).global_args(
            '-loglevel',
            'error')
        ffmpeg.run(stream, overwrite_output=True)

    def set_sound(self, audio_name, video_name):
        """set sound to mp4"""
        audio_stream = ffmpeg.input(audio_name)
        video_stream = ffmpeg.input(video_name)
        tmp_video = "tmp" + video_name
        ffmpeg.concat(
            video_stream,
            audio_stream,
            v=1,
            a=1).output(tmp_video).global_args(
            '-loglevel',
            'error').run(
            overwrite_output=True)
        os.remove(video_name)
        shutil.copy2(tmp_video, video_name)
        os.remove(tmp_video)

    def mosaic(self, img, alpha=0.1):
        w = img.shape[1]
        h = img.shape[0]
        alpha_w = int(w * alpha)
        alpha_h = int(h * alpha)
        img = cv2.resize(img, (alpha_w, alpha_h))
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)
        return img

    def get_frame_itr(self):
        def _iterator():
            while self.cap.grab():
                yield self.cap.retrieve()[1]
        return tqdm(
            _iterator(),
            total=int(self.cap.get(CAP_PROP_FRAME_COUNT)))

    def clip(self, start, end):
        """
        Cut out the video by specifying the start and end seconds.
        """
        stream = ffmpeg.input(self.input_video, ss=start, to=end)
        stream = ffmpeg.output(
            stream, self.output_video).global_args(
            '-loglevel', 'error')
        ffmpeg.run(stream, overwrite_output=True)
