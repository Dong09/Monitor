import cv2
from tool.monitor_utils import *
import datetime
import re


# cap = cv2.VideoCapture(f'./data/3/2021061111.mp4')


# success, frame = cap.read()

# while success:
    
#     cv2.imshow("Wmain",frame)
#     key = cv2.waitKey(1)
#     if key == ord("s") or key == ord("S"):
#         cv2.imwrite('./data/2.png',frame)
#     success, frame = cap.read()




# compare_color('./data/2.png',('red','grey'))
# print(len('2021-06-16 11:03:10'))

a = datetime.datetime.now()
a = str(a)
x = a[:19]
print(x)

a = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
print(a)
time.sleep(2)
b = datetime.datetime.now()

print(type(b-a))
print(str(b-a))

# time = '2021061111'

# time_name = time[:4] + '-' + time[4:6] + '-' + time[6:8] + ' ' + time[8:10] + ':' + '00:31.373114'

# print(time_name)