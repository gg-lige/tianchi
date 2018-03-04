import cv2
import os

#所有数据的标注文件

DATA_DIR = "E:\\competition\\tianchi\\tianchi"

# IM_ROWS = 5106
IM_ROWS = 4000
IM_COLS = 15106
ROI_SIZE = 512
import numpy as np
def on_mouse(event, x, y, flags, params):
    img, points = params['img'], params['points']
    if event == cv2.EVENT_FLAG_LBUTTON:  #左键点击
        points.append((x, y))

    if event == cv2.EVENT_FLAG_RBUTTON:  #右键点击
        points.pop()

    temp = img.copy()
    if len(points) > 2:
        cv2.fillPoly(temp, [np.array(points)], (0, 0, 255))  #填充多边形，(图像，多边形点形成的数组，颜色RGB)

    for i in range(len(points)):
        cv2.circle(temp, points[i], 1, (0, 0, 255)) #画圆（图像、圆心、半径、颜色）

    cv2.circle(temp, (x, y), 1, (0, 255, 0))
    cv2.imshow('img', temp)  #显示图像

def label_img(img,img1, label_name):
    c = 'x'
    tiny = np.zeros(img.shape)
    while c != 'n':
        cv2.namedWindow('img', 0)  #创建一个窗口，名字为 img
        cv2.namedWindow('img_2015', 0)
        temp = img.copy()
        points = []
        cv2.setMouseCallback('img', on_mouse, {'img': temp, 'points': points}) #鼠标响应；（窗口的名字；鼠标响应函数/回调函数；传给回调函数的参数）
        cv2.imshow('img', img)
        cv2.imshow('img_2015', img1)
        c = chr(cv2.waitKey(0))

        if c == 's':
            if len(points) > 0:
                cv2.fillPoly(img, [np.array(points)], (0, 0, 255))
                cv2.fillPoly(tiny, [np.array(points)], (255, 255, 255))
    print(label_name)
    cv2.imwrite(label_name, tiny)
    return

if __name__ == '__main__':
    for i in range(int(IM_ROWS // ROI_SIZE)+1):
        for j in range(int(IM_COLS // ROI_SIZE)):
            ss1_2017 = '{}/mylabel2/2017_{}_{}_{}_.jpg'.format(DATA_DIR, i, j, ROI_SIZE)
            ss1_2015 = '{}/mylabel2/2015_{}_{}_{}_.jpg'.format(DATA_DIR, i, j, ROI_SIZE)
            ss2 = '{}/mylabel3/{}_{}_{}_.jpg'.format(DATA_DIR, i, j, ROI_SIZE)
            if os.path.exists(ss2):
                continue
            src = cv2.imread(ss1_2017, cv2.IMREAD_UNCHANGED)
            src2 = cv2.imread(ss1_2015, cv2.IMREAD_UNCHANGED)
            label_img(src,src2, ss2)