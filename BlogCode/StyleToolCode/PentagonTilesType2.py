# -*- coding:cp936 -*-
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
from math import sin, radians
import random


"""--------------------------------------"""
"""--------��������------"""


def conver_point2polgon(a_list):
    """����ͨ�ĵ�����ת���ɿ�������Ҫ�ص���"""
    point_obj = [arcpy.Point(i[0], i[1]) for i in a_list]
    polygon = arcpy.Polygon(arcpy.Array(point_obj))
    return polygon


def check_extent(input_layer):
    """
    ��ȡ����ͼ�㣨Ҫ�������դ�񣩵ĳߴ�
    :param input_layer: ����ͼ��
    :return: ԭ�㣬����
    """
    lyr = arcpy.mapping.Layer(input_layer)
    lyr_e = lyr.getExtent()
    _origin = (lyr_e.XMin, lyr_e.YMin)
    # ((35437617.0031, 3373897.8944), 52000.0, 52000.0)
    return _origin, lyr_e.width, lyr_e.height, lyr_e.spatialReference


def tile_creator(array_obj, featurecalss):
    """
    ��ȡ���е�һ������Σ�����ȡÿ��������е�һ���㣬����ת��Ϊ arcpy.Point ���󣬶��
    arcpy.Point ����ת��Ϊ  arcpy.Array ����Ȼ��ʹ��  arcpy.Array ���󴴽�
    arcpy.Polygon ���ζ�����󽫼��ζ��������Ҫ����
    :param array_obj:������������ε��б�
    :param featurecalss: ���ʸ���ļ�
    :return:
    """
    inser_cursor = arcpy.da.InsertCursor(featurecalss, "SHAPE@")
    
    for polygon1 in array_obj:
        # for x, y in polygon1:
        #     print x
        #     print y
        points = [arcpy.Point(x, y) for x, y in polygon1]
        # print points
        # sys.exit()
        arcpy_array = arcpy.Array(points)
        inser_cursor.insertRow([arcpy.Polygon(arcpy_array)])
        # print "Inserted"
        
    del inser_cursor



arcpy.AddMessage("\n|---------------------------------|")
arcpy.AddMessage(" -----  ������ GIS�� ����������  ------")
arcpy.AddMessage("|---------------------------------|\n")

"""--------��������------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------��������------"""

"""--------������ӿ�------"""
"""--------������ӿ�------"""
input_fc = arcpy.GetParameterAsText(0)  # featureclass
output_fc = arcpy.GetParameterAsText(1)  # featureclass
side_length = int(arcpy.GetParameterAsText(2))
long_side_length = int(arcpy.GetParameterAsText(3))
num = int(arcpy.GetParameterAsText(4))  # x,y����չ����
# ������
# input_fc = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb" \
#            r"\Export_Output_2 "
# output_fc = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb\Output_e"
# side_length = 100
# long_side_length = 200
# num = 2

ws = os.path.dirname(output_fc)
fc_name = os.path.basename(output_fc)
# arcpy.env.scratchWorkspace = ws
"""--------������ӿ�------"""
"""--------������ӿ�------"""

# ws = os.path.abspath(os.getcwd())
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

# ����ԭ��
# lyr_o, lyr_w, lyr_h, sr=check_extent("data/grid.shp")
lyr_o, lyr_w, lyr_h, sr = check_extent(input_fc)
print "featureclass width:{}".format(lyr_w)
print "featureclass ht:{}".format(lyr_h)
origin = lyr_o
oX = origin[0]
oY = origin[1]
print "origin X:{}".format(oX)
print "origin Y:{}".format(oY)

# �Ƕ�
angle01 = 60
# ����ζ̱߳���
# length = 600
length = side_length
# ���߳��ȣ�x �᷽��߳����ȣ�
leng = length * sin(radians(angle01)) * 2
# �� ��y �᷽��߳��߶ȣ�û��Լ����

# ht = leng*2

ht = long_side_length
cfm = arcpy.CreateFeatureclass_management
# shpfile = cfm(ws, "PentagonTile2", "polygon", spatial_reference=sr)
shpfile = cfm(ws, fc_name + "012047", "polygon", spatial_reference=sr)

"""--------��������------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------��������------"""
# �����������һ��

# �ϰ벿��
pta = (oX + leng, oY)
ptb = (pta[0], ht + oY)
ptc = (oX + leng / 2, ht + oY + length / 2)
ptd = (oX, oY + ht)
pte = origin

# �°벿��
pta2 = (pta[0], pta[1])
ptb2 = (ptb[0], oY - ht)
ptc2 = (ptc[0], oY - ht - length / 2)
ptd2 = (oX, oY - ht)
pte2 = origin

pts = [pta, ptb, ptc, ptd, pte,
       pta2, ptb2, ptc2, ptd2, pte2]

"""--------��������------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------����Ҫ��------"""
# ƫ�ƾ���
# ���ϽǾ���

offset_x = -leng / 2

offset_y = ht * 2 + length / 2

# ���ҷ���ƫ��

offset_x2 = leng
offset_y2 = 0

# test
# A = pts[:5]
# B = pts[5:]
# print A
# print B
# tile_creator([B], shpfile) # TODO [B]���У�B����
# test

# y�᷽��ѭ������

loop_y = int(lyr_h / (ht * 2 + length))
print loop_y
array_pt = []  # ���ڴ��һ���е������

# for i in xrange(int(loop_y*1.2)):
for i in xrange(int(loop_y * num)):
    # ����ƫ�ƾ���
    new_pts = [(_[0] + offset_x * i, _[1] + offset_y * i) for _ in pts]
    
    A = new_pts[:5]
    B = new_pts[5:]
    array_pt.append(A)
    array_pt.append(B)

arcpy.AddMessage("Start to Ccreate Geometry...")
loop_x = int(lyr_w / leng)
# ��չ����
for _ in xrange(int(loop_x * num)):
    tile_creator(array_pt, shpfile)
    # array_pt = [[(12613045.67822186, 2643673.2934923917),
                # (12613045.67822186, 2643873.2934923917),
                # (12612959.075681482, 2643923.2934923917),
                # (12612872.473141104, 2643873.2934923917),
                # (12612872.473141104, 2643673.2934923917)],
                #
                # [(12613045.67822186, 2643673.2934923917),
                # (12613045.67822186, 2643473.2934923917),
                # (12612959.075681482, 2643423.2934923917),
                # (12612872.473141104, 2643473.2934923917),
                # (12612872.473141104, 2643673.2934923917)]]
    # �б���ÿһ������������Ӻ��ٷ�װ���б�
    array_pt2 = []
    for point_list in array_pt:
        
        pointss = [(xx+offset_x2, xy+offset_y2) for xx, xy in point_list]
        array_pt2.append(pointss)
    array_pt = array_pt2
    
    # np_array = np_array + (offset_x2, offset_y2)

"""--------����Ҫ��------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------ɾ����Χ���Ҫ��------"""
arcpy.AddMessage("Geometry Created")
feature_layer = "f_layer"
try:
    arcpy.MakeFeatureLayer_management(shpfile, feature_layer)
except UnicodeEncodeError:
    arcpy.AddError("\n����ArcMap�汾�ľ��ޣ���ʹ�ô�Ӣ�����·����")
arcpy.SelectLayerByLocation_management(feature_layer,
                                       "INTERSECT", input_fc)
arcpy.CopyFeatures_management(feature_layer, output_fc)
arcpy.Delete_management(shpfile)

# arcpy.env.mask = input_fc
# arcpy.CopyFeatures_management(shpfile, output_fc)

arcpy.AddMessage("Geometry Cliped")
arcpy.AddMessage("Finshed")
"""--------ɾ����Χ���Ҫ��------"""
"""--------------------------------------"""
