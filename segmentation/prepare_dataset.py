import os
import cv2
import sys
import copy
import json
import shutil
from collections import defaultdict
import random
import numpy as np
from PIL import Image
from tqdm.auto import tqdm
from glob import glob
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

upper_clothes = ["탑", "블라우스", "티셔츠", "니트웨어", "셔츠"]
lower_clothes = ["청바지", "팬츠", "조거팬츠"]
dicts = {"Training": "train", "Validation": "valid"}


def extract_data(method: str) -> None:
    json_paths = glob(os.path.join(method, '*', '*.json'))
    image_paths = defaultdict(list)

    for json_path in tqdm(json_paths):
        flag = False

        with open(json_path, 'r') as f:
            datas = json.load(f)

        orders = ["긴팔", "반팔", "스커트", "바지"]
        tmp = {"긴팔": None, "반팔": None, "스커트": None, "바지": None}

        h, w = datas["이미지 정보"]["이미지 높이"], datas["이미지 정보"]["이미지 너비"]
        detail = datas["데이터셋 정보"]["데이터셋 상세설명"]
        shirt = detail["라벨링"]["상의"][0]
        pants = detail["라벨링"]["하의"][0]
        upper_mask = np.zeros((h, w), dtype=np.uint8)
        lower_mask = np.zeros((h, w), dtype=np.uint8)

        if len(shirt) > 0:
            if shirt.get('기장') == "노멀":
                # print(shirt)
                if shirt.get("카테고리") in upper_clothes:
                    polygon_data = detail["폴리곤좌표"]["상의"][0]
                    polygon_data = sorted(polygon_data.items(), key=lambda x: (int(x[0][3:]), x[0]))
                    polys = []

                    for i in range(0, len(polygon_data), 2):
                        x1, y1 = int(polygon_data[i][1]), int(polygon_data[i+1][1])
                        polys.append([x1, y1])

                    polys = np.array(polys)
                    if shirt.get("소매기장") == "긴팔" and len(polys) > 0:
                        upper_mask = cv2.fillPoly(upper_mask, [polys], color=1)
                        tmp["긴팔"] = upper_mask
                        # print(upper_mask.sum())
                        flag = True
                    elif shirt.get("소매기장") == "반팔" and len(polys) > 0:
                        upper_mask = cv2.fillPoly(upper_mask, [polys], color=1)
                        tmp["반팔"] = upper_mask
                        # print(upper_mask.sum())
                        flag = True

        if len(pants) > 0:
            if pants.get("카테고리") == "스커트":
                polygon_data = detail["폴리곤좌표"]["하의"][0]
                polygon_data = sorted(polygon_data.items(), key=lambda x: (int(x[0][3:]), x[0]))
                polys = []

                for i in range(0, len(polygon_data), 2):
                    x1, y1 = int(polygon_data[i][1]), int(polygon_data[i+1][1])
                    polys.append([x1, y1])

                polys = np.array(polys)
                if len(polys) > 0:
                    cv2.fillPoly(lower_mask, [polys], color=1)
                    tmp["스커트"] = lower_mask
                    flag = True
                
            elif pants.get("카테고리") in lower_clothes and pants.get("기장") == "발목":
                polygon_data = detail["폴리곤좌표"]["하의"][0]
                polygon_data = sorted(polygon_data.items(), key=lambda x: (int(x[0][3:]), x[0]))
                polys = []

                for i in range(0, len(polygon_data), 2):
                    x1, y1 = int(polygon_data[i][1]), int(polygon_data[i+1][1])
                    polys.append([x1, y1])

                polys = np.array(polys)
                if len(polys) > 0:
                    cv2.fillPoly(lower_mask, [polys], color=1)
                    tmp["바지"] = lower_mask
                    flag = True

        if flag:
            result = []
            for o in orders:
                if tmp.get(o) is not None:
                    _img = tmp.get(o)
                    _img = _img.astype(np.uint8)
                    result.append(_img)
                else:
                    result.append(np.zeros((h, w), dtype=np.uint8))

            result = np.array(result, dtype=np.uint8)
            result = result.transpose(1, 2, 0)
            root = '/'.join(json_path.split('/')[:-1])
            name = json_path.split('/')[-1][:-5]
            shutil.copy(os.path.join(root, f"{name}.jpg"), f'dataset/valid/images/{name}.jpg')

            _img = Image.fromarray(result)
            _img.save(f"dataset/valid/labels/{name}.png")


if __name__ == '__main__':
    extract_data("Validation")
