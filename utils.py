import math
from pathlib import Path
import os
import glob
from shutil import copy
from PIL import Image

def extract_img_to_dataset(hr_source_path, lr_source_path, hr_to_path, lr_to_path, lr_source_scale='x2', total=5000, ext='.jpg',category_ratios=[
    {"category": "百货", "ratio": 0.1, "exclude":[]},
    {"category": "电器", "ratio": 0.1, "exclude": []},
    {"category": "家纺", "ratio": 0.1, "exclude": []},
    {"category": "美妆", "ratio": 0.1, "exclude": []},
    {"category": "母婴", "ratio": 0.1, "exclude": []},
    {"category": "男装", "ratio": 0.05, "exclude": []},
    {"category": "内衣", "ratio": 0.1, "exclude": []},
    {"category": "女装", "ratio": 0.05, "exclude": []},
    {"category": "食品", "ratio": 0.1, "exclude": []},
    {"category": "首饰", "ratio": 0.1, "exclude": []},
    {"category": "鞋包", "ratio": 0.05, "exclude": []},
    {"category": "运动", "ratio": 0.05, "exclude": []},
]):
    if total <= 0:
        return

    #目标目录是否存在
    if not Path(hr_to_path).exists():
        os.makedirs(hr_to_path)

    if not Path(lr_to_path).exists():
        os.makedirs(lr_to_path)

    for item in category_ratios:
        count = math.floor(total*item["ratio"])

        hr_category_dir = os.path.join(hr_source_path ,item["category"])
        hr_brand_dir_list = os.listdir(hr_category_dir)

        i = 0
        is_next_category = False
        for hr_brand_dir in hr_brand_dir_list:
            if hr_brand_dir == '.DS_Store' or (len(item["exclude"])>0 and hr_brand_dir in item["exclude"]):
                continue

            hr_img_list = glob.glob(os.path.join(hr_category_dir, hr_brand_dir, '*' + ext))
            for hr_img in hr_img_list:
                if i > count:
                    is_next_category = True
                    break

                hr_img_split = os.path.basename(hr_img).split('.')
                lr_img = os.path.join(lr_source_path, item["category"], os.path.basename(hr_brand_dir), lr_source_scale,
                             hr_img_split[0] + lr_source_scale + "." + hr_img_split[1])

                if not is_valid_file(hr_img):
                    os.remove(hr_img)
                    os.remove(lr_img)
                    continue

                # 赋值到目标文件目录
                copy(hr_img, hr_to_path)
                copy(lr_img, lr_to_path)
                i+=1

            if is_next_category:
                break

#判断文件是否损坏
def is_valid_file(path):
    valid = True
    try:
        Image.open(path).load()
    except OSError:
        valid =  False
    return valid

if __name__ == '__main__':
    # 训练集合抽取
    extract_img_to_dataset('D:\source\datasets\\vip_good_images\HR',
                           'D:\source\datasets\\vip_good_images\LR',
                           'D:\source\datasets\VIPGOODJPEG\VIPGOODJPEG_train_HR',
                           'D:\source\datasets\VIPGOODJPEG\VIPGOODJPEG_train_LR\X2',
                           total=0,
                           category_ratios=[
                               {"category": "百货", "ratio": 0.1, "exclude":[]},
                               {"category": "电器", "ratio": 0.1, "exclude": []},
                               {"category": "家纺", "ratio": 0.1, "exclude": []},
                               {"category": "美妆", "ratio": 0.1, "exclude": []},
                               {"category": "母婴", "ratio": 0.1, "exclude": []},
                               {"category": "男装", "ratio": 0.05, "exclude": []},
                               {"category": "内衣", "ratio": 0.1, "exclude": []},
                               {"category": "女装", "ratio": 0.05, "exclude": []},
                               {"category": "食品", "ratio": 0.1, "exclude": []},
                               {"category": "首饰", "ratio": 0.1, "exclude": []},
                               {"category": "鞋包", "ratio": 0.05, "exclude": []},
                               {"category": "运动", "ratio": 0.05, "exclude": []},
                           ])

    # 测试集合抽取
    # extract_img_to_dataset('D:\source\datasets\\vip_good_images\HR',
    #                        'D:\source\datasets\\vip_good_images\LR',
    #                        'D:\source\datasets\\benchmark\VipGoodJpegCollectTest\HR',
    #                        'D:\source\datasets\\benchmark\VipGoodJpegCollectTest\LR_bicubic\X2',
    #                        total=36,
    #                        category_ratios=[
    #                            {"category": "百货", "ratio": 0.1, "exclude": []},
    #                            {"category": "电器", "ratio": 0.1, "exclude": []},
    #                            {"category": "家纺", "ratio": 0.1, "exclude": []},
    #                            {"category": "美妆", "ratio": 0.1, "exclude": []},
    #                            {"category": "母婴", "ratio": 0.1, "exclude": []},
    #                            {"category": "男装", "ratio": 0.05, "exclude": []},
    #                            {"category": "内衣", "ratio": 0.1, "exclude": []},
    #                            {"category": "女装", "ratio": 0.05, "exclude": []},
    #                            {"category": "食品", "ratio": 0.1, "exclude": []},
    #                            {"category": "首饰", "ratio": 0.1, "exclude": []},
    #                            {"category": "鞋包", "ratio": 0.05, "exclude": []},
    #                            {"category": "运动", "ratio": 0.05, "exclude": []},
    #                        ])