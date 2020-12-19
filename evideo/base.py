import cv2
from cv2 import CAP_PROP_FRAME_COUNT
from tqdm import tqdm
import os
import ffmpeg
import shutil

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

    def get_mp3(self, audio_name, input_video=None):
        if input_video != None:
            
        stream = ffmpeg.input(self.input_video)
        stream = ffmpeg.output(stream, audio_name).global_args('-loglevel', 'error')
        ffmpeg.run(stream)

    def set_mp3(self, audio_name, video_name):
        audio_stream = ffmpeg.input(audio_name)
        video_stream = ffmpeg.input(video_name)
        tmp_video = "tmp"+video_name
        stream = ffmpeg.output(video_stream, audio_stream, tmp_video)
        ffmpeg.run(stream)
        #shutil.copyfile(tmp_video, video_nam)
        #os.remove(tmp_video)
        #if os.path.exists(self.output_video):
        #clip_output = mp.VideoFileClip(self.output_video).subclip()
        #clip_output.write_videofile(self.output_video, audio=audio_name)
        #else:
        #    raise Exception("CANNOT SET MP3 to MP4, NOT FOUND VIDEO FILE!")
        
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
        stream = ffmpeg.output(stream, self.output_video).global_args('-loglevel', 'error')
        ffmpeg.run(stream)
        #stream = ffmpeg.crop(self.ffmpeg_stream, upper_left_x, upper_left_y, width, height)
