from evideo.audio import Audio
from evideo.base import Video
import glob

mp3_file = "sample.mp3"
output_video = "amp_sample.mp4"
video_ = Video("sample.mp4", output_video=output_video)
#video_ = Video("sample.mp4")
video_.clip(0, 15)
video_.get_mp3(mp3_file)
audio_ = Audio(mp3_file)
audio_.amplify()
video_.set_mp3(mp3_file, output_video)


#video_ = Video("amp_sample.mp4")
#video_.get_mp3("sample.mp3")
#audio_ = Audio("sample.mp3")
#video_files = glob.glob("seto/*.mp4")
#for v in video_files:
#    video_ = Video(v)
#    video_.get_mp3("sample.mp3")
#    audio_ = Audio("sample.mp3")
