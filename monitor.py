from os import name
import cv2
from tool.utils import *
from tool.torch_utils import *
from tool.darknet2pytorch import Darknet
import tool.folder_operation as folder 
import argparse
import numpy as np
import datetime

"""hyper parameters"""
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



def cut_person(img, boxes, savename=None):
    import cv2
    img = np.copy(img)

    width = img.shape[1]
    height = img.shape[0]
    for i in range(len(boxes)):
        box = boxes[i]
        x1 = int(box[0] * width)
        y1 = int(box[1] * height)
        x2 = int(box[2] * width)
        y2 = int(box[3] * height)

        print('========================================================',x1,x2,y1,y2)
        target = img[y1:y2,x1:x2]
        # img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 1)
        if savename is None:
            _name = str(datetime.datetime.now().microsecond)
            print("save plot results to %s" % _name +'.jpg')
            cv2.imwrite('./data/split/'+ _name +'.jpg', target)
            folder.create_folder('./data/split/')




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


    sized = cv2.resize(imgfile, (m.width, m.height))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)

    for i in range(2):
        start = datetime.time()
        boxes = do_detect(m, sized, 0.4, 0.6, use_cuda)
        finish = datetime.time()

    cut_person(imgfile, boxes[0])
    return plot_boxes_cv2(imgfile, boxes[0], class_names=class_names),boxes[0]


def get_args():
    parser = argparse.ArgumentParser('Test your image or video by trained model.')
    parser.add_argument('-cfgfile', type=str, default= './cfg/yolov4.cfg',
                        help= './cfg/yolov4.cfg', dest='cfgfile')
    parser.add_argument('-weightfile', type=str,
                        default= './weights\\yolov4.weights',
                        help='--todo--', dest='weightfile')
    parser.add_argument('-imgfile', type=str,
                        default= './data\\WIN_20210525_09_49_39_Pro.mp4',
                        help= './data\\WIN_20210525_09_49_39_Pro.mp4', dest='imgfile')
    args = parser.parse_args()

    return args





def target_detect():
    '''
    针对目标每一帧截取图片
    '''
    cap = cv2.VideoCapture('./data/WIN_20210525_09_49_39_Pro.mp4')

    video_width = int(cap.get(3))
    video_height = int(cap.get(4))
    fps = int(cap.get(5))
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))
    
    ## ##
    def decode_fourcc(cc):
        return "".join([chr((int(cc) >> 8 * i) & 0xFF) for i in range(4)])
    ## ##
    
    # print(video_width,video_height,fps,decode_fourcc(codec))


    # videoWriter = cv2.VideoWriter('detected.mp4',cv2.VideoWriter_fourcc('a','v','c','1'),fps,(video_width,video_height))


    # while 1:
    ret,frame = cap.read()

    # cv2.imshow('cap',frame)
    print('==========================',type(frame))
    ### ###
    args = get_args()
    new_frame,boxes = detect_cv2(args.cfgfile, args.weightfile, frame)
    


    # cv2.save('./data/')

    # cv2.imshow('cap',new_frame)

    # k = cv2.waitKey(fps)
    # if k == ord('q' or 'Q'):
    #     break

    cap.release()
    cv2.destroyAllWindows()









if __name__ == '__main__':
    target_detect()
    # init_camera()
