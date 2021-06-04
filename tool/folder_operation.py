import os
import re

def create_folder(path):
    for file in os.listdir(path):
        name = re.split(r'.jpg', file)
        n = name[0]
        
        new_path = path + n + '/'

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


def get_folder_name(file):
    name = re.split('.jpg', file)
    return name[0]





if __name__ == '__main__':
    path = 'python\Deep Learning\Monitor\data\split\\'
    # create_folder(path)
    create_folder('./data/split/')
    
    print(get_folder_name('608676.jpg'))