from os import name
import cv2
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import tool.folder_operation as folder 
import argparse
import numpy as np
import datetime
import threading
from tool.monitor_utils import *






def _main(path=None):
    cap = cv2.VideoCapture('./data/WIN_20210525_09_49_39_Pro.mp4')

    video_width = int(cap.get(3))
    video_height = int(cap.get(4))
    fps = int(cap.get(5))
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))
    
    # ## ##
    # def decode_fourcc(cc):
    #     return "".join([chr((int(cc) >> 8 * i) & 0xFF) for i in range(4)])
    # print(video_width,video_height,fps,decode_fourcc(codec))
    # ## ##

    # cv2.imshow('cap',frame)
    # print('==========================',frame)
    ### ###

    
    args = get_args()
    timeF = 50  #视频帧计数间隔频率
    c = 0
    
    while cap.isOpened():   #循环读取视频帧
        
        ret,frame = cap.read()
        # cv2.imshow('s',frame)
        if(c%timeF == 0): #每隔timeF帧进行存储操作
            # cv2.imshow('s',frame)
            new_frame,boxes = detect_cv2(args.cfgfile, args.weightfile, frame)
        c = c + 1
        cv2.waitKey(5)

    cap.release()
        



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
    _main()
    # init_camera()
