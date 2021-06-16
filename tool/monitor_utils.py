import cv2
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import argparse
import datetime
import threading
import random
import time
from recogn import *
import asyncio
from tool.time_operate import *

### ###
use_cuda = False


def init_camera():
    try:
        capture = cv2.VideoCapture(0)
        while(True):
            # 获取一帧
            ret, frame = capture.read()
            # 将这帧转换为灰度图
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', frame)
            # 如果输入q，则退出
            if cv2.waitKey(1) == ord('q'):
                break
    except e:
        print(e)



def cutperson(img, boxes, savename=None):
    import cv2
    img = np.copy(img)

    width = img.shape[1]
    height = img.shape[0]
    for i in range(len(boxes)):
        box = boxes
        x1 = int(box[0] * width) if int(box[0] * width)>=0 else 0
        y1 = int(box[1] * height) if int(box[1] * height)>=0 else 0
        x2 = int(box[2] * width) if int(box[2] * width)>=0 else 0
        y2 = int(box[3] * height) if int(box[3] * height)>=0 else 0
        class_names = load_class_names('./data/coco.names')
        print('len///////////////////////',len(img))
        
        if len(box) >= 7 and class_names :
            cls_conf = box[5]
            cls_id = box[6]

            # if class_names[cls_id] == 'person' and cls_conf>=0.8:
            print('========================================================',x1,x2,y1,y2)
            target = img[y1:y2,x1:x2]

            return target




def get_args():
    parser = argparse.ArgumentParser('Test your image or video by trained model.')
    parser.add_argument('-cfgfile', type=str, default= './cfg/yolov4.cfg',
                        help= './cfg/yolov4.cfg', dest='cfgfile')
    parser.add_argument('-weightfile', type=str,
                        default= './weights\\yolov4.weights',
                        help='--todo--', dest='weightfile')
    parser.add_argument('-imgfile', type=str,
                        default= '\data\WIN_20210525_09_56_56_Pro.mp4',
                        help= '\data\WIN_20210525_09_56_56_Pro.mp4', dest='imgfile')
    args = parser.parse_args()

    return args



def rectangle_save_person(img, box,areaid,time,result_path='',start_time=''):
    import cv2
    img = np.copy(img)

    width = img.shape[1]
    height = img.shape[0]

    x1 = int(box[0] * width) if int(box[0] * width)>=0 else 0
    y1 = int(box[1] * height) if int(box[1] * height)>=0 else 0
    x2 = int(box[2] * width) if int(box[2] * width)>=0 else 0
    y2 = int(box[3] * height) if int(box[3] * height)>=0 else 0
    class_names = load_class_names('./data/coco.names')
    print('len///////////////////////',len(img))
    
    if len(box) >= 7 and class_names :
        cls_conf = box[5]
        cls_id = box[6]

        # if class_names[cls_id] == 'person' and cls_conf>=0.8:
        print('========================================================',x1,x2,y1,y2)
        target = img[y1:y2,x1:x2]

        img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        check_time = datetime.datetime.now()
        print(type(start_time))
        # temp = start_time[:19]
        # print(temp)

        # start_time = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")
        substraction_time =  check_time - start_time
        print(str(substraction_time)[2:])
        
        ###
        time_name = time[:4] + '-' + time[4:6] + '-' + time[6:8] + ' ' + time[8:10] + ':' + str(substraction_time)[2:]
        print(time_name)
        a = datetime.datetime.strptime(time_name, "%Y-%m-%d %H:%M:%S")
        a = time_operate_poor(a)

        #### TODO
        cv2.imwrite(f'{result_path}{a}{areaid.zfill(2)}.jpg', img)

        return check_time






def searchbydress(image, colorid=0):
    '''
    return : tuple in the list 
    For exmple: [('red','blue'),('green','pink'),]
    '''
    import cv2
    cfgfile = './cfg/yolov4.cfg'
    weightfile = './weights\\yolov4.weights'

    m = Darknet(cfgfile)

    m.print_network()
    m.load_weights(weightfile)
    # print('Loading weights from %s... Done!' % (weightfile))
    if use_cuda:
        m.cuda()

    # print('-------------------------',m.num_classes)
    num_classes = m.num_classes
    if num_classes == 20:
        namesfile =  './data/voc.names'
    elif num_classes == 80:
        namesfile =  './data/coco.names'
    else:
        namesfile =  './data/coco.names'
    class_names = load_class_names(namesfile)

    # ## TODO
    # image = cv2.imread(image)
    sized = cv2.resize(image, (m.width, m.height))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

    for i in range(2):
        start = time.time()
        boxes = do_detect(m, sized, 0.4, 0.6, use_cuda)
        finish = time.time()

    # print(boxes)

    res = []
    if len(boxes[0]) != 0:
        # print(boxes)
        for i in range(len(boxes[0])):
            temp = []
            # print(boxes[0])
            person = cutperson(image, boxes[0][i])
            # print(person.shape)
            height = person.shape[0]
            wide = person.shape[1]
            cloth1 = person[:height//2,:wide]
            cloth2 = person[height//2:,:wide]
            temp.append(hsv_color(cloth1))
            temp.append(hsv_color(cloth2))
            res.append(tuple(temp))
            # cv2.imshow('p',person[:height,int(1/6*wide):int(wide-1/6*wide)])

        return res,boxes[0]
    else:
        return [('no','no'),] , boxes[0]
        


def compare_color(image,areaid,time,result_path='',colorid=('',''),start_time=''):
    '''
    image: origin image 
    colorid: string in tuple
    return: True or False  , time_now
    '''
    res_cloth_list , box = searchbydress(image)

    # color_dict = {'black': 0, 'grey':1 ,'white': 2, 'red':3 , 'orange': 4, 'yellow': 5, 'green': 6, 'cyan': 7, 'blue': 8, 'purple': 9}
    # color_list = ['black', 'grey' ,'white', 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']

    # for key,value in color_dict.items():
    #     if cloth1 == key:
    #         if value == colorid[0]:
    #             print('c1 check')
    #     if cloth2 == key:
    #         if value == colorid[1]:
    #             print('c2 check')

    # print(res_cloth_list)
    # print(colorid)
    # print(box)
    for i in range(len(res_cloth_list)):
        temp = res_cloth_list[i]

        if temp[0] == 'red' or temp[0] == 'red2':
            temp[0] = 'red'
            if (temp[0],temp[1]) == colorid:
                print('check')
                check_time = rectangle_save_person(image, box[i], areaid, time,result_path,start_time=start_time)
                return True  , check_time 
            else:
                time_now = datetime.datetime.now()
                return False  , time_now 
                # cv2.save('./data/')
        elif (temp[0],temp[1]) == colorid:
                print('check')
                check_time = rectangle_save_person(image, box[i], areaid, time,result_path,start_time=start_time)
                return True  , check_time
        else:
            time_now = datetime.datetime.now()
            return False  , time_now 

            






if __name__ == '__main__':
    compare_color('./data/1.png','3')