from evideo.audio import Audio
from evideo.base import Video

video_ = Video("VID20201217190606.mp4", output_video="sample.mp4")
#video_.clip(0, 10)
video_.get_mp3("sample.mp3")
audio_ = Audio("sample.mp3")
