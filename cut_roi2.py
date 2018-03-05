from collections import defaultdict
import csv
import sys
import cv2  #openCV 官方扩展库
# from shapely.geometry import MultiPolygon, Polygon
# import shapely.wkt
# import shapely.affinity
import numpy as np  #处理大型矩阵
import tifffile as tiff   #标签图像文件格式（Tag Image File Format，简写为TIFF）是一种灵活的位图格式，主要用来存储包括照片和艺术图在内的图像
import matplotlib.pyplot as plt
from matplotlib import cm

"""
同时切分2015、2017年的图像，图像大小为256像素，
"""


FILE_2015 = 'E:\\competition\\tianchi\\20171105_quarterfinals\\quarterfinals_2015.tif'
FILE_2017 = 'E:\\competition\\tianchi\\20171105_quarterfinals\\quarterfinals_2017.tif'
# FILE_cadastral2015 = '../../preliminary/cadastral2015.tif'
# FILE_tinysample = '../../preliminary/tinysample.tif'

#tifffile的图片的读取顺序height×width×channels。R,G,B，近红 按照波段来获取。
im_2015 = tiff.imread(FILE_2015).transpose([1, 2, 0])  #参数为维度索引,(高，宽，通道数4)
im_2017 = tiff.imread(FILE_2017).transpose([1, 2, 0])

# im_tiny = tiff.imread(FILE_tinysample)
# im_cada = tiff.imread(FILE_cadastral2015)
print(im_2015.shape)  #查看形状，表明是一个4000*15106*4的矩阵
print(im_2017.shape)


#将图片的像素值放缩到[0,1]之间
def scale_percentile(matrix):
    w, h, d = matrix.shape
    matrix = np.reshape(matrix, [w * h, d]).astype(np.float64)
    # Get 2nd and 98th percentile
    mins = np.percentile(matrix, 1, axis=0)  # 百分位数是统计中使用的度量，表示小于这个值得观察值占某个百分比。（输入数组，要计算的百分位数0-100之间，沿着它计算百分位树的轴）
    maxs = np.percentile(matrix, 99, axis=0) - mins
    matrix = (matrix - mins[None, :]) / maxs[None, :]
    matrix = np.reshape(matrix, [w, h, d])
    matrix = matrix.clip(0, 1) # clip这个函数将将数组中的元素限制在a_min, a_max之间，大于a_max的就使得它等于 a_max，小于a_min,的就使得它等于a_min。
    # print(matrix)
    return matrix


img_size = 256 # 15106/ 256   5106/256

for i in range(int(len(im_2015)/img_size) + 1 ): # last 284
    for j in range(int(len(im_2015[0])/img_size) ): #last 2 too small, drop one
        im_name = str(i)+'_'+str(j)+'_'+str(img_size)+'_.jpg'   #几行几列图形大小
        cv2.imwrite("2017_"+im_name,scale_percentile(im_2017[i*img_size:i*img_size+img_size, j*img_size:j*img_size+img_size, :3])*255)
        cv2.imwrite("2015_"+im_name,scale_percentile(im_2015[i*img_size:i*img_size+img_size, j*img_size:j*img_size+img_size, :3])*255)
        # cv2.imwrite("cada/"+im_name,im_cada[i*img_size:i*img_size+img_size, j*img_size:j*img_size+img_size]*255)
        # cv2.imwrite("tiny/"+im_name,im_tiny[i*img_size:i*img_size+img_size, j*img_size:j*img_size+img_size]*255)

