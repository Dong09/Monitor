from multiprocessing.context import Process
from os import name
import cv2
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import tool.folder_operation as folder 
import argparse
import numpy as np
import datetime
from tool.monitor_utils import *
from threading import Thread , Lock 



def CameraCapture():
    global IMAGE,isend,mutex

    #摄像头
    cap = cv2.VideoCapture("./data/2/2021_05_25_10.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

    #捕获视频
    success, frame = cap.read()
    index = 1
    while success:
        cv2.imshow("Wmain",frame)

        if index == fps:
            mutex.acquire()
            IMAGE = frame.copy()
            mutex.release()
            index = 1

        index += 1

        key =  cv2.waitKey(int(1000//fps))
        if key == ord("q") or key == ord("Q"):
            isend = True
            break

        success, frame = cap.read()

    #释放资源
    cv2.destroyAllWindows()
    cap.release()




def detectByRoll(path=None):
    '''
    detectByRoll
    '''
    global IMAGE,isend
    print('detectByRoll  begin')
    while not isend:
        if IMAGE is None:
            continue
        print(IMAGE.shape)
        frame = IMAGE.copy()
        compare_color(frame,colorid=('red','gray'))

        

def main():
    capture = Thread(target=CameraCapture)
    detect = Thread(target=detectByRoll)

    capture.start()
    detect.start()

    capture.join()
    detect.join()



    # cv2.save('./data/')

    # cv2.imshow('cap',new_frame)

    # k = cv2.waitKey(fps)
    # if k == ord('q' or 'Q'):
    #     break

    # try:
    #     th1 = threading.Thread(detect_cv2(cfgfile, weightfile, imgfile),args=('th1'))
    #     th1 = threading.Thread(detect_cv2(cfgfile, weightfile, imgfile),args=('th1'))
    # except:
    #     print('error')




if __name__ == '__main__':
    IMAGE = None
    mutex = Lock()
    isend = False
    main()
    # init_camera()
