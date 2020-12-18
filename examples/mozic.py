import cv2
from cv2 import CAP_PROP_FRAME_COUNT
from evideo.base import Base
from mtcnn import MTCNN

video_filename = "input/clip.mp4"


base = Base(video_filename)
detector = MTCNN()
faces_all = []
for frame in base.get_frame_itr():
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(color)
    faces_all.append(faces)

del base
del detector

base = Base(video_filename, outfilename="mozaic_mtcnn.mp4" )
for i, frame in enumerate(base.get_frame_itr()):
    for face in faces_all[i]:
        x, y, w, h = face["box"]
        if x <= 0 or y <= 0 or w <= 0 or h <= 0:
            continue
        frame[y:y+h, x:x+w] = base.mosaic(frame[y:y+h, x:x+w])
    base.writer.write(frame)
    
