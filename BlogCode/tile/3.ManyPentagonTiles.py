# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              tile
# Author:            Hygnic
# Created on:        2021/7/22 11:11
# Version:           
# Reference:         120°, 120°, 120°, 120°, 60°
# V3.3.3.3.6
"""
Description:         构建多个整体
Usage:               
"""
# -------------------------------------------
from __future__ import absolute_import
from __future__ import division
import os
import arcpy
from pprint import pprint
import numpy as np
from math import pi, exp, cos, sin, radians

"""---------------------"""
"""---------基本属性-----------"""
ws = os.path.abspath(os.getcwd())
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

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

lyr_o, lyr_w, lyr_h, sr=check_extent("data/grid.shp")


# 坐标原点
origin = lyr_o
oX = origin[0]
oY = origin[1]
print "origin X:".format(oX)
print "origin Y:".format(oY)
length = 300
angle01 = 60

"""---------基本属性-----------"""
"""---------------------"""

# 垂直距离
leng = length * sin(radians(angle01))  # 300*sin60°
# double_length = length*2

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



"""---------------------"""
"""--------构建要素------"""



def conver_point2Polgon(a_list):
    """将普通的点数据转换成可以制作要素的面"""
    point_obj = [arcpy.Point(i[0], i[1]) for i in a_list]
    polygon = arcpy.Polygon(arcpy.Array(point_obj))
    return polygon


cfm = arcpy.CreateFeatureclass_management
shpfile = cfm(ws, "PentagonTile", "polygon", spatial_reference=sr)

# 循环创建20次
loop = int(lyr_h/(6*leng))
array_pt = []
for i in xrange(loop*2):
    new_pts = [(_[0] - length * 3 / 2 * 1 * i, _[1] + 5 * leng * 1 * i) for _ in pts]

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



"""--------构建要素------"""
"""---------------------"""

np_array = np.array(array_pt)
print "Len:{}".format(len(np_array)) # 396
print "Size:{}".format(np_array.size)
print "Shape:{}".format(np_array.shape)
print "Ndim:{}".format(np_array.ndim)
# pprint(np_array)
offset_x2 = -length*4.5
offset_y2 = -leng
np_array = np_array-(offset_x2,offset_y2)

loop = int(lyr_w/(4*length))
for i in xrange(loop*2):
    rows = arcpy.da.InsertCursor(shpfile, "SHAPE@")
    for ii in np_array:
        pprint(ii)
        # 不需要转换了，支持np.array格式
        # poly = conver_point2Polgon(ii)
        rows.insertRow([ii])