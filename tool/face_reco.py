from PIL import Image, ImageDraw
import face_recognition
import cv2
import os


def get_frame_image(video_path, out_image_folder_path, frame_frequency):
    """

    视频解析为图片到指定文件夹
    :param video_path:视频路径
    :param out_image_folder_path:解析后的图片文件夹路径
    :param frame_frequency:帧数(每多少帧读解析一张图片)
    :return:
    """
    if not os.path.exists(out_image_folder_path):
        os.makedirs(out_image_folder_path)
    # 加载视频文件
    cap = cv2.VideoCapture(video_path)
    # 帧数
    times = 0
    while True:
        times += 1
        res, image = cap.read()
        if not res:
            break
        if times % frame_frequency == 0:
            cv2.imwrite(out_image_folder_path + str(times) + '.jpg', image)


# get_image('data/WIN_20210525_09_49_39_Pro.mp4', 'data/image/', 100)


def draw_box(image, location, name='Target'):
    '''

    :param image: Frame image to be retrieved(path)待检索帧图片
    :param location: Face position(top, right, bottom, left)比对人脸位置
    :param name: Name of the lost person
    :return: Search result image
    '''
    if location:
        unknown_image = face_recognition.load_image_file(image)

        top, right, bottom, left = location
        # Create a PIL imagedraw object so we can draw on the picture
        pil_image = Image.fromarray(unknown_image)
        draw = ImageDraw.Draw(pil_image)
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        del draw
        pil_image.show()
        pil_image.save("image_with_boxes.jpg")
    else:
        print('No missing persons were found!')


def create_folder(areaid, time, filename):
    '''
    areaid: areaid (string)
    time: time (string) (e: 20210616)
    filename: name of file is usually time (string)
    path: need a filename , create the folder for it
    '''
    new_path = './' + 'data/' + areaid + 'check/' + filename + '/'

    isExists=os.path.exists(new_path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(new_path)
        print(new_path+' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(new_path+' 目录已存在')

    return new_path

