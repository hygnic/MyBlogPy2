# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              tile
# Author:            Hygnic
# Created on:        2021/7/22 11:11
# Version:           
# Reference:         120°, 120°, 120°, 120°, 60°
                     # V3.3.3.3.6
"""
Description:         构建单个五边形瓦片的面要素
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
origin = (0, 0)
o_x = origin[0]
o_y = origin[1]
length = 300
angle01 = 60

"""---------基本属性-----------"""
"""---------------------"""

# 垂直距离
leng = length * sin(radians(angle01)) # 300*sin60°

point_a = (o_x + length*2, o_y)
point_b = (point_a[0] + length / 2, leng)
point_c = (point_a[0], leng*2)
point_d = (length, point_c[1])

point_e = (length/2, leng*3)

five_points = [origin ,point_a, point_b, point_c, point_d]

print point_a
print point_b
print point_c
print point_d
print point_e



"""---------------------"""
"""--------构建要素------"""
point_obj = [arcpy.Point(i[0], i[1]) for i in five_points]
polygon = arcpy.Polygon(arcpy.Array(point_obj))


cfm = arcpy.CreateFeatureclass_management
shpfile = cfm(ws, "SingleTile", "polygon")
rows = arcpy.da.InsertCursor(shpfile, "SHAPE@")
rows.insertRow([polygon])



"""--------构建要素------"""
"""---------------------"""

