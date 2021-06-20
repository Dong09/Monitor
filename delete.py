import cv2
from tool.monitor_utils import *
import datetime
import re
import face_recognition 
from tool.time_operate import *
from tool.database import *


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

# a = datetime.datetime.now()
# a = str(a)
# x = a[:19]
# print(x)

# a = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
# print(a)
# time.sleep(2)
# b = datetime.datetime.now()

# print(type(b-a))
# print(str(b-a))

# time = '2021061111'

# time_name = time[:4] + '-' + time[4:6] + '-' + time[6:8] + ' ' + time[8:10] + ':' + '00:31.373114'

# print(time_name)








def drawface(img, boxes,areaid,time,result_path='',start_time=''):
    import cv2
    img = np.copy(img)

    width = img.shape[1]
    height = img.shape[0]
    for i in range(len(boxes)):
        box = boxes
        x1 = int(box[0])
        y1 = int(box[1])
        x2 = int(box[2])
        y2 = int(box[3])
        # class_names = load_class_names('./data/coco.names')
        print('len///////////////////////',len(img))

        # if class_names[cls_id] == 'person' and cls_conf>=0.8:
        print('========================================================',x1,x2,y1,y2)
        target = img[x1:x2,y2:y1]

        img = cv2.rectangle(img, (y1,x1), (y2,x2), (0, 0, 255), 2)
        
        # cv2.imshow('sdf',img)
        # cv2.waitKey(0)
        
        check_time = datetime.datetime.now()
        print(type(start_time))

        substraction_time =  check_time - start_time
        print(str(substraction_time)[2:7])
        
        ###
        time_name = time[:4] + '-' + time[4:6] + '-' + time[6:8] + ' ' + time[8:10] + ':' + str(substraction_time)[2:7]
        print(time_name)
        a = datetime.datetime.strptime(time_name, "%Y-%m-%d %H:%M:%S")
        time_copy = a 
        a = time_operate_poor(a)
        
        # print(f'{result_path}{a}{areaid.zfill(2)}.jpg')
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        cv2.imwrite(f'{result_path}{a}{areaid.zfill(2)}.jpg', img)

        return time_copy




def searchbyface(image,areaid,time,result_path='',start_time=''):
    '''
    :param image: Frame image to be retrieved(path)待检索帧图片
    :param face: Face image to be compared(path)人脸对比图片
    :return: Compare the frame image with the face image,if it is the same person, return to the face position人脸位置
    '''
    global IMAGE,isend
    print('searchbyface  begin')
    
    # print(type(frame))
    frame = face_recognition.load_image_file('./data/face/frame.jpg')
    face = face_recognition.load_image_file('./data/face/face.jpg')

    image_locations = face_recognition.face_locations(frame, number_of_times_to_upsample=0, model="hog")
    print(image_locations)

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
        pass
    else:
        check_time = drawface(frame, location,areaid=areaid,time=time,start_time=start_time,result_path=result_path)
        # print(check_time.year)

        video_time = time_operate_db(check_time)
        search_time = time_operate_db(start_time)

        db_operate('facesearch', (search_time,int(areaid),0,video_time,'./data/face/',result_path) )




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



start_time = datetime.datetime.now()
time_folder = time_operate_poor(start_time)
result_path = folder.create_folder('3',time_folder)

searchbyface('./data/face/face.jpg','3','2021061811',result_path=result_path,start_time=start_time)








# a = []

# print(a[0])