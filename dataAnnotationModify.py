import cv2
import os

"""
标注过一遍后，检查标注文件的正确性，只生成新标记出的数据，位于mylabel_2017_mod_2/ 中
打开2015，2017，上次标签三张图片 进行重新检查
"""
DATA_DIR = "E:\\competition\\tianchi\\tianchi"

# IM_ROWS = 5106
IM_ROWS = 4000
IM_COLS = 15106
ROI_SIZE = 256
import numpy as np
def on_mouse(event, x, y, flags, params):
    img, points = params['img'], params['points']
    if event == cv2.EVENT_FLAG_LBUTTON:
        points.append((x, y))

    if event == cv2.EVENT_FLAG_RBUTTON:
        points.pop()

    temp = img.copy()
    if len(points) > 2:
        cv2.fillPoly(temp, [np.array(points)], (0, 0, 255))

    for i in range(len(points)):
        cv2.circle(temp, points[i], 1, (0, 0, 255))

    cv2.circle(temp, (x, y), 1, (0, 255, 0))
    cv2.imshow('img', temp)

def label_img(img,img1,label, label_name):
    c = 'x'
    tiny = np.zeros(img.shape)
    while c != 'n':
        cv2.namedWindow('img', 0)
        cv2.namedWindow('img_2015', 0)
        cv2.namedWindow('img_label', 0)
        temp = img.copy()
        points = []
        cv2.setMouseCallback('img', on_mouse, {'img': temp, 'points': points})
        cv2.imshow('img', img)
        cv2.imshow('img_2015', img1)
        cv2.imshow('img_label', label)
        c = chr(cv2.waitKey(0))

        if c == 's':
            if len(points) > 0:
                cv2.fillPoly(img, [np.array(points)], (0, 0, 255))
                cv2.fillPoly(tiny, [np.array(points)], (255, 255, 255))

        if c == 'x':
            cv2.imwrite(label_name, tiny)
            break

    print(label_name)

    return

if __name__ == '__main__':

   for i in range(int(IM_ROWS // ROI_SIZE)+1):   #//表示不管操作数为何种数值类型，总是会舍去小数部分，返回数字序列中比真正的商小的最接近的数字。行数0-11
        for j in range(int(IM_COLS // ROI_SIZE)):#列数0-58
            ss1_2017 = '{}/2017/2017_{}_{}_{}_.jpg'.format(DATA_DIR, i, j, ROI_SIZE)
            ss1_2015 = '{}/2017/2015_{}_{}_{}_.jpg'.format(DATA_DIR, i, j, ROI_SIZE)
            label = '{}/mylabel_2017/{}_{}_{}_.jpg'.format(DATA_DIR, i, j, ROI_SIZE)
            ss2 = '{}/mylabel_2017_mod_2/{}_{}_{}_.jpg'.format(DATA_DIR, i, j, ROI_SIZE) #再次检查时，需要添加的标签
            if os.path.exists(ss2):
                continue
            src = cv2.imread(ss1_2017, cv2.IMREAD_UNCHANGED)  #2017年数据
            src2 = cv2.imread(ss1_2015, cv2.IMREAD_UNCHANGED)   #2015年数据
            src3 = cv2.imread(label, cv2.IMREAD_UNCHANGED)  #我们添加的标注样例
            label_img(src,src2,src3, ss2)