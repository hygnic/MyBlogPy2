# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              tile
# Author:            Hygnic
# Created on:        2021/7/22 11:11
# Version:           
# Reference:

"""
Description:
            完全构建五边形密铺。
            
            五边形类型：
            120°, 120°, 120°, 120°, 60°
            # V3.3.3.3.6
            https://en.wikipedia.org/wiki/File:1-uniform_10_dual_color1.png


Usage:               
"""
# -------------------------------------------
from __future__ import absolute_import
from __future__ import division
import os
import arcpy
import numpy as np
from math import sin, radians, pow, sqrt


"""--------------------------------------"""
"""--------基本方法------"""

# def conver_point2polgon(a_list):
#     """将普通的点数据转换成可以制作要素的面"""
#     point_obj = [arcpy.Point(i[0], i[1]) for i in a_list]
#     polygon = arcpy.Polygon(arcpy.Array(point_obj))
#     return polygon

def check_extent(input):
    """
    获取输入图层本身的尺寸
    :param input: 输入图层地址
    :return: 原点，宽，高
    """
    lyr = arcpy.mapping.Layer(input)
    lyr_extent = lyr.getExtent()
    _origin = (lyr_extent.XMin, lyr_extent.YMin)
    if lyr.isRasterLayer:
        # arcpy.env.extent = lyr_extent
        # arcpy.env.mask = lyr
        pass
        
    return _origin, lyr_extent.width, \
               lyr_extent.height, lyr_extent.spatialReference


def tile_creator(array_obj, featurecalss):
    """
    将 array_obj 中的点去除然后生成面
    :param array_obj:
    :param featurecalss: 矢量文件
    :return:
    """
    _rows = arcpy.da.InsertCursor(featurecalss, "SHAPE@")
    for _ii in array_obj:
        _rows.insertRow([_ii])
    del _rows


"""--------基本方法------"""
"""--------------------------------------"""


"""--------------------------------------"""
"""--------基本属性------"""

ws = os.path.abspath(os.getcwd())
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True


# 坐标原点
# lyr_o, lyr_w, lyr_h, sr=check_extent("data/grid.shp")
lyr_o, lyr_w, lyr_h, sr=check_extent("tiff.tif")
print "featureclass width:{}".format(lyr_w)
print "featureclass height:{}".format(lyr_h)
origin = lyr_o
oX = origin[0]
oY = origin[1]
print "origin X:{}".format(oX)
print "origin Y:{}".format(oY)
# 五边形短边长度
length = 300
# 角度
angle01 = 60

# 垂直距离
leng = length * sin(radians(angle01))  # 300*sin60°

"""--------基本属性------"""
"""--------------------------------------"""




"""--------------------------------------"""
"""--------基本坐标------"""
#一组五边形在坐标四个象限内的坐标

pta = (oX + length * 2, oY)
ptb = (pta[0] + length / 2, oY + leng)
ptc = (pta[0], oY + leng * 2)
ptd = (oX + length, ptc[1])
pte = (oX + length / 2, oY + leng * 3)
quadrant1 = [origin, pta, ptb, ptc, ptd, pte]

# 二象限
pta2 = (oX - length * 2, pta[1])
ptb2 = (pta2[0] - length / 2, ptb[1])
ptc2 = (pta2[0], ptc[1])
ptd2 = (oX - length, ptd[1])
pte2 = (oX - length / 2, pte[1])
quadrant2 = [origin, pta2, ptb2, ptc2, ptd2, pte2]

# 三象限
ptb3 = (ptb2[0], oY - leng)
ptc3 = (ptc2[0], oY - leng * 2)
ptd3 = (ptd2[0], ptc3[1])
pte3 = (pte2[0], oY - leng * 3)
quadrant3 = [origin, pta2, ptb3, ptc3, ptd3, pte3]

# 四象限
ptb4 = (pta[0] + length / 2, oY - leng)
ptc4 = (pta[0], oY - leng * 2)
ptd4 = (oX + length, ptc4[1])
pte4 = (oX + length / 2, oY - leng * 3)
quadrant4 = [origin, pta, ptb4, ptc4, ptd4, pte4]

pts = [origin, pta, ptb, ptc, ptd, pte,
       origin, pta2, ptb2, ptc2, ptd2, pte2,
       origin, pta2, ptb3, ptc3, ptd3, pte3,
       origin, pta, ptb4, ptc4, ptd4, pte4]


# A = quadrant1[:-1]
# B = quadrant1[4:]+[quadrant2[5],quadrant2[4],origin]
# C = quadrant2[:-1]
# D = quadrant3[:-1]
# E = quadrant3[4:]+[quadrant4[5],quadrant4[4],origin]
# F = quadrant4[:-1]

"""--------基本坐标------"""
"""--------------------------------------"""




"""--------------------------------------"""
"""--------构建要素------"""
# 重要参数和属性

cfm = arcpy.CreateFeatureclass_management
shpfile = cfm(ws, "PentagonTile", "polygon", spatial_reference=sr)

# 左上方向的偏移距离
offset_x = -length * 3/2
offset_y =  5 * leng
# 右下方向的偏移距离
offset_x2 = length*4.5
offset_y2 = -leng

# ratio = lyr_h/(5*leng)
# new_width = length * 3/2 * ratio
# new_hieght= lyr_h
# distance = sqrt(pow(new_width,2) + pow(new_hieght, 2))
# print new_width
# print new_hieght
# print distance

# y轴方向循环次数
loop_y = int(lyr_h/(6*leng))
array_pt = [] # 用于存放一整列的五边形
for i in xrange(int(loop_y*1.6)):
    # 向上偏移距离
    # new_pts = [(_[0] - length * 3 / 2 * i, _[1] + 5 * leng * i) for _ in pts]
    new_pts = [(_[0]+offset_x*i, _[1]+offset_y*i) for _ in pts]

    A = new_pts[:5]
    B = new_pts[4:6] + [new_pts[11], new_pts[10], new_pts[0]]
    C = new_pts[6:11]
    D = new_pts[12:17]
    E = new_pts[16:18] + [new_pts[-1], new_pts[-2], new_pts[0]]
    F = new_pts[-6:-1]
    array_pt.append(A)
    array_pt.append(B)
    array_pt.append(C)
    array_pt.append(D)
    array_pt.append(E)
    array_pt.append(F)

np_array = np.array(array_pt)
print "Len:{}".format(len(np_array)) # 396
print "Size:{}".format(np_array.size)
print "Shape:{}".format(np_array.shape)
print "Ndim:{}".format(np_array.ndim)

loop_x = int(lyr_w/(4*length))
for _ in xrange(int(loop_x*1.4)):
    tile_creator(np_array, shpfile)
    np_array = np_array+(offset_x2, offset_y2)

"""--------构建要素------"""
"""--------------------------------------"""
    