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
import time as T
import tool.folder_operation as folder 



def CameraCapture(areaid,time,isreal,sec):
    '''
    replay the video 

    time: string
    areaid: string
    '''
    global IMAGE,isend,mutex

    #摄像头
    cap = cv2.VideoCapture(f'./data/{areaid}/{time}.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    c = 1
    index = 1
    print(fps)

    #捕获视频
    success, frame = cap.read()
    while success:
        if isreal:
            if index == int(fps):
                cv2.imshow("Wmain",frame)
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
        else:
            frameRate = int(fps) * sec 
            if(c % frameRate == 0):
                cv2.imshow("Wmain",frame)
                if IMAGE.qsize()<=10 :
                    try:
                        # print('in->')
                        mutex.acquire()
                        IMAGE.put(frame.copy())
                        mutex.release()
                    except:
                        break
            c += 1
        # print(IMAGE.qsize())

        

        key =  cv2.waitKey(int(1000//fps))
        if key == ord("q") or key == ord("Q"):
            isend = True
            break

        success, frame = cap.read()

    #释放资源
    cv2.destroyAllWindows()
    cap.release()




def detectByRoll(cloth1,cloth2,areaid,time,path='',start_time=''):
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
            ischeck , check_time = compare_color(frame,areaid,time,result_path=path,colorid=(cloth1,cloth2),start_time=start_time)
            if ischeck :
                # print()
                check_time = time_operate_db(check_time)
                print((check_time,int(areaid),0,time,cloth1,cloth2,path))
                # searchtime areaid isreal videotime dressinfo1 dressinfo2 resultpath
                # db_operate('dresssearch', (check_time,0,0,check_time,cloth1,cloth2,'./data') )





def division_func(areaid,time,isreal,sec,search_type,colorid=('',''),result_path='',start_time=''):
    capture = Thread(target=CameraCapture,args=(areaid,time,isreal,sec,))
    detect = Thread(target=search_type,args=(colorid[0],colorid[1],areaid,time,result_path,start_time,))

    capture.start()
    detect.start()

    capture.join()
    detect.join()






#############################################################################################

def searchinareas(areaid,time,result_path='',start_time='',isreal=False,use='face',image=None,colorid=('',''),sec=1):
    if not isreal:
        division_func(areaid, time, isreal, sec, detectByRoll, colorid,result_path,start_time)
    else:
        division_func(areaid, time, isreal, sec, detectByRoll, colorid,result_path,start_time)

















if __name__ == '__main__':
    IMAGE = Queue(maxsize=30)
    mutex = Lock()
    isend = False
    areaid = '3'

    start_time = datetime.datetime.now()
    time_folder = time_operate_poor(start_time)
    result_path = folder.create_folder(areaid,time_folder)
    print(result_path)

    searchinareas(areaid,'2021061111',colorid=('orange','gray'),result_path=result_path,start_time=start_time)

    # IMAGE = Queue(maxsize=30)
    # mutex = Lock()
    # isend = False
    # main()

    # init_camera()
