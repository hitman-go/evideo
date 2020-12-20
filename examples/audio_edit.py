from evideo.audio import Audio
from evideo.base import Video

mp3_file = "sample.mp3"
output_video = "amp_sample.mp4"

# get mp3 from mp4
video_ = Video("sample.mp4", output_video=output_video)
video_.clip(start=0, end=15)
video_.get_mp3(mp3_file, output_video)

audio_ = Audio(mp3_file)
# amplify mp3 file
audio_.amplify()

# set mp3 to mp4
video_.set_mp3(mp3_file, output_video)
