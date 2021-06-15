import cv2
from tool.monitor_utils import *


# cap = cv2.VideoCapture(f'./data/3/2021061111.mp4')


# success, frame = cap.read()

# while success:
    
#     cv2.imshow("Wmain",frame)
#     key = cv2.waitKey(1)
#     if key == ord("s") or key == ord("S"):
#         cv2.imwrite('./data/2.png',frame)
#     success, frame = cap.read()




compare_color('./data/2.png',('red','grey'))