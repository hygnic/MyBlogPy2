# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              4.ManyPentagonTilesType2
# Author:            Hygnic
# Created on:        2021/7/23 14:21
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
from __future__ import absolute_import
from __future__ import division
import os
import arcpy
import numpy as np
from math import sin, radians



"""--------------------------------------"""
"""--------基本方法------"""

def conver_point2polgon(a_list):
    """将普通的点数据转换成可以制作要素的面"""
    point_obj = [arcpy.Point(i[0], i[1]) for i in a_list]
    polygon = arcpy.Polygon(arcpy.Array(point_obj))
    return polygon

def check_extent(input):
    """
    获取输入图层本身的尺寸
    :param input: 输入图层地址
    :return: 原点，宽，高
    """
    lyr = arcpy.mapping.Layer(input)
    lyr_extent = lyr.getExtent()
    _origin = (lyr_extent.XMin, lyr_extent.YMin)
    # ((35437617.0031, 3373897.8944), 52000.0, 52000.0)
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


"""--------工具箱接口------"""
"""--------工具箱接口------"""
fc = arcpy.GetParameterAsText(0) # featureclass
output_fc = arcpy.GetParameterAsText(1) # featureclass
side_length = int(arcpy.GetParameterAsText(2))
long_side_length = int(arcpy.GetParameterAsText(3))
num = int(arcpy.GetParameterAsText(4)) # x,y轴扩展倍数

ws = os.path.dirname(output_fc)
fc_name = os.path.basename(output_fc)
# arcpy.env.scratchWorkspace = ws
"""--------工具箱接口------"""
"""--------工具箱接口------"""


# ws = os.path.abspath(os.getcwd())
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

# 坐标原点
# lyr_o, lyr_w, lyr_h, sr=check_extent("data/grid.shp")
lyr_o, lyr_w, lyr_h, sr=check_extent(fc)
print "featureclass width:{}".format(lyr_w)
print "featureclass ht:{}".format(lyr_h)
origin = lyr_o
oX = origin[0]
oY = origin[1]
print "origin X:{}".format(oX)
print "origin Y:{}".format(oY)

# 角度
angle01 = 60
# 五边形短边长度
# length = 600
length = side_length
# 长边长度（x 轴方向边长长度）
leng = length * sin(radians(angle01))*2
# 高 （y 轴方向边长高度，没有约束）

# ht = leng*2

ht = long_side_length
cfm = arcpy.CreateFeatureclass_management
# shpfile = cfm(ws, "PentagonTile2", "polygon", spatial_reference=sr)
shpfile = cfm(ws, fc_name, "polygon", spatial_reference=sr)

"""--------基本属性------"""
"""--------------------------------------"""



"""--------------------------------------"""
"""--------基本坐标------"""
# 该五边形两个一组

# 上半部分
pta = (oX + leng, oY)
ptb = (pta[0], ht + oY)
ptc = (oX + leng / 2, ht + oY + length / 2)
ptd = (oX, oY + ht)
pte = origin

# 下半部分
pta2 = (pta[0], pta[1])
ptb2 = (ptb[0], oY - ht)
ptc2 = (ptc[0], oY - ht - length / 2)
ptd2 = (oX, oY - ht)
pte2 = origin

pts = [pta, ptb, ptc, ptd, pte,
       pta2, ptb2, ptc2, ptd2, pte2]

"""--------基本坐标------"""
"""--------------------------------------"""



"""--------------------------------------"""
"""--------构建要素------"""
# 偏移距离
# 右上角距离

offset_x = -leng/2

offset_y = ht*2+length/2

# 正右方向偏移

offset_x2 = leng
offset_y2 = 0


# test
# A = pts[:5]
# B = pts[5:]
# print A
# print B
# tile_creator([B], shpfile) # TODO [B]就行，B不行
# test

# y轴方向循环次数

loop_y = int(lyr_h / (ht * 2 + length))
print loop_y
array_pt = [] # 用于存放一整列的五边形

# for i in xrange(int(loop_y*1.2)):
for i in xrange(int(loop_y*num)):
    # 向上偏移距离
    new_pts = [(_[0]+offset_x*i, _[1]+offset_y*i) for _ in pts]

    A = new_pts[:5]
    B = new_pts[5:]
    array_pt.append(A)
    array_pt.append(B)

np_array = np.array(array_pt)
print "Len:{}".format(len(np_array))
print "Size:{}".format(np_array.size)
print "Shape:{}".format(np_array.shape)
print "Ndim:{}".format(np_array.ndim)

loop_x = int(lyr_w/leng)
# for _ in xrange(int(loop_x*1.15)):
for _ in xrange(int(loop_x*num)):
    tile_creator(np_array, shpfile)
    np_array = np_array+(offset_x2, offset_y2)

"""--------构建要素------"""
"""--------------------------------------"""
