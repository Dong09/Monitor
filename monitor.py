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
from tool.face_reco import *



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




def detectByRoll(cloth1,cloth2,areaid,start_time,time,path=''):
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
            ischeck , real_time = compare_color(frame,areaid,time,result_path=path,colorid=(cloth1,cloth2),start_time=start_time)
            if ischeck :
                # print()
                real_time = time_operate_db(real_time)
                check_time = time_operate_poor_p(time)
                dressinfo1 = cloth_color_convert(cloth1)
                dressinfo2 = cloth_color_convert(cloth2)

                print((real_time,int(areaid),0,check_time,cloth1,cloth2,path))
                # searchtime areaid isreal videotime dressinfo1 dressinfo2 resultpath
                db_operate('dresssearch', (str(real_time),int(areaid),0,check_time,dressinfo1,dressinfo2,path) )




def searchbyface(image,areaid,time,start_time,result_path=''):
    '''
    :param image: Frame image to be retrieved(path)待检索帧图片
    :param face: Face image to be compared(path)人脸对比图片
    :return: Compare the frame image with the face image,if it is the same person, return to the face position人脸位置
    '''
    global IMAGE,isend
    print('searchbyface  begin')
    while not isend:
        if IMAGE.qsize() == 0 :
            continue
        else:
            # print(IMAGE.qsize())
            frame = IMAGE.get()

        # print(type(frame))
        face = face_recognition.load_image_file(image)

        image_locations = face_recognition.face_locations(frame, number_of_times_to_upsample=0, model="hog")
        # print(image_locations)

        try:
            face_encoding = face_recognition.face_encodings(face)[0]
            image_encoding = face_recognition.face_encodings(frame, image_locations)
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            quit()

        known_face_encodings = [
            face_encoding
        ]
        location = sub_searchbyface(image_locations, image_encoding, known_face_encodings)
        print(location)

        if location == None:
            continue
        else:
            drawface(frame, location,areaid=areaid,time=time,start_time=start_time,result_path=result_path)





def sub_searchbyface(image_locations,image_encoding,known_face_encodings):
    for image_location, unknown_encoding_to_check in zip(image_locations, image_encoding):
        matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding_to_check)
        print(matches)
        # print(face_recognition.face_distance(known_face_encodings, unknown_encoding_to_check))
        if matches[0]:
            print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>{image_location}')
            return image_location
        else:
            continue





def division_func(areaid,time,start_time,isreal,use,sec,search_type,image,colorid=('',''),result_path=''):
    capture = Thread(target=CameraCapture,args=(areaid,time,isreal,sec,))
    if use == 'face':
        detect = Thread(target=search_type,args=(image,areaid,time,result_path,start_time,))
    else:
        detect = Thread(target=search_type,args=(colorid[0],colorid[1],areaid,time,result_path,start_time,))

    capture.start()
    detect.start()

    capture.join()
    detect.join()






#############################################################################################

def searchinareas(areaid,time,start_time,result_path='',isreal=False,use='face',image='',colorid=('',''),sec=1):
    if not isreal:
        if use == 'face':
            division_func(areaid, time, start_time ,isreal, use , sec, searchbyface, image , result_path , ) 
        else:
            division_func(areaid, time, start_time ,isreal, use , sec, detectByRoll, colorid , result_path , )

















if __name__ == '__main__':
    IMAGE = Queue(maxsize=30)
    mutex = Lock()
    isend = False
    areaid = '3'

    start_time = datetime.datetime.now()
    time_folder = time_operate_poor(start_time)
    result_path = folder.create_folder(areaid,time_folder)
    print(result_path)
    image = './data/face/face.jpg'

    searchinareas(areaid,'2021061111',start_time=start_time,use='face',colorid=('orange','gray'),result_path=result_path,image=image)

    # IMAGE = Queue(maxsize=30)
    # mutex = Lock()
    # isend = False
    # main()

    # init_camera()
