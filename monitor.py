from multiprocessing.context import Process
from os import name
import cv2
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import tool.folder_operation as folder 
from tool.database import *
from tool.time_operate import *
import argparse
import numpy as np
import datetime
from tool.monitor_utils import *
from threading import Thread , Lock 
from queue import Queue



def CameraCapture(time,areaid):
    '''
    replay the video 

    time: string
    areaid: string
    '''
    global IMAGE,isend,mutex

    #摄像头
    cap = cv2.VideoCapture(f'./data/{areaid}/{time}.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

    #捕获视频
    success, frame = cap.read()
    index = 1
    while success:
        cv2.imshow("Wmain",frame)
        # print(IMAGE.qsize())

        if index == int(fps):
            if IMAGE.qsize()<=10 :
                try:
                    # print('in->')
                    mutex.acquire()
                    IMAGE.put(frame.copy())
                    mutex.release()
                except:
                    break
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




def detectByRoll(path,cloth1,cloth2):
    '''
    detectByRoll
    '''
    global IMAGE,isend
    print('detectByRoll  begin')
    print(cloth1,cloth2)
    while not isend:
        if IMAGE.qsize() == 0 :
            continue
        else:
            # print(IMAGE.qsize())
            frame = IMAGE.get()
            # ORIGIN IMAGE IS frame
            ischeck , check_time = compare_color(frame,colorid=(cloth1,cloth2))
            if ischeck :
                check_time = time_operate(check_time)
                print((check_time,0,0,check_time,cloth1,cloth2,'./data'))
                # searchtime areaid isreal videotime dressinfo1 dressinfo2 resultpath
                # db_operate('dresssearch', (check_time,0,0,check_time,cloth1,cloth2,'./data') )





def main():
    capture = Thread(target=CameraCapture,args=('2021061111','3',))
    detect = Thread(target=detectByRoll,args=("./data/3/2021061111.mp4",'red','gray',))

    capture.start()
    detect.start()

    capture.join()
    detect.join()




def replayVideo(areaid,time):
    #摄像头
    cap = cv2.VideoCapture(f'./data/{areaid}/{time}.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

    #捕获视频
    success, frame = cap.read()
    index = 1
    while success:
        cv2.imshow("Wmain",frame)
    
        success, frame = cap.read()

    #释放资源
    cv2.destroyAllWindows()
    cap.release()





#############################################################################################

def searchinareas(areaid,time,isreal=True,use='face',image=None,colorid=(None,None),sec=5):
    if not isreal:
        replayVideo(areaid,time)

















if __name__ == '__main__':
    searchinareas('3','2021061111')

    # IMAGE = Queue(maxsize=30)
    # mutex = Lock()
    # isend = False
    # main()

    # init_camera()
