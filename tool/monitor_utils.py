import cv2
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import tool.folder_operation as folder 
import argparse
import datetime
import threading
import random
import time
from recogn import *

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
        box = boxes[i]
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
                # img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 1)
                # if savename is None:
                #     rand = str(int(random.random()*10000))
                #     _name = str(datetime.datetime.now().microsecond)
                #     print("save plot results to %s" %_name +'.jpg')
                #     cv2.imwrite('./data/split/'+ _name + rand +'.jpg', target)
                #     folder.create_folder('./data/split/')



def detect_cv2(cfgfile, weightfile, imgfile):
    import cv2
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


    if len(imgfile) != 0 or imgfile is not None:
        
        sized = cv2.resize(imgfile, (m.width, m.height))
        sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

        for i in range(2):
            start = time.time()
            boxes = do_detect(m, sized, 0.4, 0.6, use_cuda)
            finish = time.time()

        cutAndCreateFolder(imgfile, boxes[0])
        return plot_boxes_cv2(imgfile, boxes[0], class_names=class_names),boxes[0]
    else:
        return 0,0


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




def searchbydress(image, colorid=0):
    '''
    return : result color
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


    sized = cv2.resize(image, (m.width, m.height))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

    for i in range(2):
        start = time.time()
        boxes = do_detect(m, sized, 0.4, 0.6, use_cuda)
        finish = time.time()

    if len(boxes[0]) != 0:
        person = cutperson(image, boxes[0])
        # print(person.shape)
        height = person.shape[0]
        wide = person.shape[1]
        cloth1 = person[:height//2,:wide]
        cloth2 = person[height//2:,:wide]
        cv2.imshow('p',person[:height,int(1/6*wide):int(wide-1/6*wide)])

        return hsv_color(cloth1),hsv_color(cloth2),image
    else:
        return None,None,None
        


def compare_color(image,colorid=None):
    cloth1,cloth2,orgin_image = searchbydress(image)

    # color_dict = {'black': 0, 'grey':1 ,'white': 2, 'red':3 , 'orange': 4, 'yellow': 5, 'green': 6, 'cyan': 7, 'blue': 8, 'purple': 9}
    # color_list = ['black', 'grey' ,'white', 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']

    # for key,value in color_dict.items():
    #     if cloth1 == key:
    #         if value == colorid[0]:
    #             print('c1 check')
    #     if cloth2 == key:
    #         if value == colorid[1]:
    #             print('c2 check')
    print(f'({cloth1},{cloth2})')
    if cloth1 == 'red' or cloth1 == 'red2':
        cloth1 = 'red'
        if (cloth1,cloth2) == colorid:
            print('check')
            print(datetime.datetime.now())
            # cv2.save('./data/')
    elif (cloth1,cloth2) == colorid:
            print('check')

            






if __name__ == '__main__':
    compare_color(image)