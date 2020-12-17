import cv2
from cv2 import CAP_PROP_FRAME_COUNT
from tqdm import tqdm
import os


class Base:
    def __init__(self, video_name, outfilename=None):
        self.cap = cv2.VideoCapture(video_name)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        if outfilename is not None:
            self.writer = cv2.VideoWriter(
                outfilename, fourcc, self.fps, (self.width, self.height))
        if os.path.exists:
            self.cascade = cv2.CascadeClassifier(
                "haarcascade_frontalface_default.xml")

    def __del__(self):
        try:
            self.writer.release()
        except BaseException:
            pass
        self.cap.release()
        cv2.destroyAllWindows()

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
        for i, frame in enumerate(self.get_frame_itr()):
            if start * self.fps <= i and end * self.fps >= i:
                self.writer.write(frame)
            elif end * self.fps < i:
                break
        return
