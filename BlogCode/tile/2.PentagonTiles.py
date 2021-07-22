# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              tile
# Author:            Hygnic
# Created on:        2021/7/22 11:11
# Version:           
# Reference:         120°, 120°, 120°, 120°, 60°
# V3.3.3.3.6
"""
Description:         构建多个个五边形瓦片,这五个形成一个整体
Usage:               
"""
# -------------------------------------------
from __future__ import absolute_import
from __future__ import division
import os
import arcpy
from math import pi, exp, cos, sin, radians

"""---------------------"""
"""---------基本属性-----------"""
ws = os.path.abspath(os.getcwd())
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

# 坐标原点
origin = (100, 1000)
oX = origin[0]
oY = origin[1]
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

A = quadrant1[:-1]
B = quadrant1[4:]+[quadrant2[5],quadrant2[4],origin]
C = quadrant2[:-1]
D = quadrant3[:-1]
E = quadrant3[4:]+[quadrant4[5],quadrant4[4],origin]
F = quadrant4[:-1]



"""---------------------"""
"""--------构建要素------"""
def conver_point2Polgon(a_list):
    point_obj = [arcpy.Point(i[0], i[1]) for i in a_list]
    polygon = arcpy.Polygon(arcpy.Array(point_obj))
    return polygon


cfm = arcpy.CreateFeatureclass_management
shpfile = cfm(ws, "PentagonTile", "polygon")
rows = arcpy.da.InsertCursor(shpfile, "SHAPE@")
for i in (A, B, C, D, E, F):
    poly = conver_point2Polgon(i)
    rows.insertRow([poly])

"""--------构建要素------"""
"""---------------------"""
