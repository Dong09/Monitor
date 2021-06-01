import os
import  cv2
import numpy as np
import tool.colorList as cl 
import tool.folder_operation as folder 

# filename='python\Deep Learning\Monitor\data\split\\611668.jpg'
path = 'python\Deep Learning\Monitor\data\split\\'
 
#处理图片
def get_color(frame,_dir):
    print('go in get_color')
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = cl.getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv,color_dict[d][0],color_dict[d][1])
        cv2.imwrite('python\Deep Learning\Monitor\data\\split\\'+ _dir + '\\' + d +'.jpg',mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        # binary = cv2.dilate(binary,None,iterations=2)
        cnts, hiera = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        # print(np.size(cnts))
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        if sum > maxsum :
            maxsum = sum
            color = d
 
    return color


if __name__ == '__main__':
    
    for file in os.listdir(path):
        if not os.path.isdir(path + file):
            frame = cv2.imread(path + file)

            folder.create_folder(path)
            _dir = folder.get_folder_name(file)
            print(_dir)

            print(get_color(frame,_dir))

    # img = cv2.imread(path + '604689\\' + 'red2.jpg')
    # print(img)