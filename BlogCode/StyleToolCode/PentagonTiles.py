# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              tile
# Author:            Hygnic
# Created on:        2021/7/22 11:11
# Version:           
# Reference:

"""
Description:
            ��ȫ������������̡�
            
            ��������ͣ�
            120��, 120��, 120��, 120��, 60��
            # V3.3.3.3.6
            https://en.wikipedia.org/wiki/File:1-uniform_10_dual_color1.png


Usage:               
"""
# -------------------------------------------
from __future__ import absolute_import
from __future__ import division
import os
import arcpy
from math import sin, radians, pow, sqrt

"""--------------------------------------"""
"""--------��������------"""


# def conver_point2polgon(a_list):
#     """����ͨ�ĵ�����ת���ɿ�������Ҫ�ص���"""
#     point_obj = [arcpy.Point(i[0], i[1]) for i in a_list]
#     polygon = arcpy.Polygon(arcpy.Array(point_obj))
#     return polygon

def check_extent(input_layer):
    """
    ��ȡ����ͼ�㱾��ĳߴ�
    :param input_layer: ����ͼ��
    :return: ԭ�㣬����
    """
    lyr = arcpy.mapping.Layer(input_layer)
    lyr_extent = lyr.getExtent()
    _origin = (lyr_extent.XMin, lyr_extent.YMin)
    # if lyr.isRasterLayer:
    #     # arcpy.env.extent = lyr_extent
    #     # arcpy.env.mask = lyr
    #     pass
    desc = arcpy.Describe(input_layer)
    # return _origin, lyr_extent.width, lyr_extent.height, lyr_extent.spatialReference
    return _origin, lyr_extent.width, lyr_extent.height, desc.spatialReference


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


"""--------��������------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------��������------"""
arcpy.AddMessage("\n|---------------------------------|")
arcpy.AddMessage(" -----  ������ GIS�� ����������  ------")
arcpy.AddMessage("|---------------------------------|\n")



ws = os.path.abspath(os.getcwd())
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

"""--------������ӿ�------"""
"""--------������ӿ�------"""
input_fc = arcpy.GetParameterAsText(0)  # featureclass
output_fc = arcpy.GetParameterAsText(1)  # featureclass
side_length = int(arcpy.GetParameterAsText(2))
num = int(arcpy.GetParameterAsText(3))  # x,y����չ����

ws = os.path.dirname(output_fc)
fc_name = os.path.basename(output_fc)
# arcpy.env.scratchWorkspace = ws
"""--------������ӿ�------"""
"""--------������ӿ�------"""

# ����ԭ��
# lyr_o, lyr_w, lyr_h, sr=check_extent("tiff.tif")
lyr_o, lyr_w, lyr_h, sr = check_extent(input_fc)
print "featureclass width:{}".format(lyr_w)
print "featureclass height:{}".format(lyr_h)
origin = lyr_o
oX = origin[0]
oY = origin[1]
print "origin X:{}".format(oX)
print "origin Y:{}".format(oY)
# ����ζ̱߳���
# length = 300
length = side_length
# �Ƕ�
angle01 = 60

# ��ֱ����
leng = length * sin(radians(angle01))  # 300*sin60��

cfm = arcpy.CreateFeatureclass_management
# shpfile = cfm(ws, "PentagonTile", "polygon", spatial_reference=sr)
shpfile = cfm(ws, fc_name + "0012701", "polygon", spatial_reference=sr)

"""--------��������------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------��������------"""
# һ��������������ĸ������ڵ�����

pta = (oX + length * 2, oY)
ptb = (pta[0] + length / 2, oY + leng)
ptc = (pta[0], oY + leng * 2)
ptd = (oX + length, ptc[1])
pte = (oX + length / 2, oY + leng * 3)
quadrant1 = [origin, pta, ptb, ptc, ptd, pte]

# ������

pta2 = (oX - length * 2, pta[1])
ptb2 = (pta2[0] - length / 2, ptb[1])
ptc2 = (pta2[0], ptc[1])
ptd2 = (oX - length, ptd[1])
pte2 = (oX - length / 2, pte[1])
quadrant2 = [origin, pta2, ptb2, ptc2, ptd2, pte2]

# ������

ptb3 = (ptb2[0], oY - leng)
ptc3 = (ptc2[0], oY - leng * 2)
ptd3 = (ptd2[0], ptc3[1])
pte3 = (pte2[0], oY - leng * 3)
quadrant3 = [origin, pta2, ptb3, ptc3, ptd3, pte3]

# ������

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

"""--------��������------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------����Ҫ��------"""

# ���Ϸ����ƫ�ƾ���

offset_x = -length * 3 / 2
offset_y = 5 * leng

# ���·����ƫ�ƾ���

offset_x2 = length * 4.5
offset_y2 = -leng

# ratio = lyr_h/(5*leng)
# new_width = length * 3/2 * ratio
# new_hieght= lyr_h
# distance = sqrt(pow(new_width,2) + pow(new_hieght, 2))
# print new_width
# print new_hieght
# print distance

# y�᷽��ѭ������

loop_y = int(lyr_h / (6 * leng))
array_pt = []  # ���ڴ��һ���е������
# for i in xrange(int(loop_y*1.6)):
for i in xrange(int(loop_y * num)):
    # ����ƫ�ƾ���
    # new_pts = [(_[0] - length * 3 / 2 * i, _[1] + 5 * leng * i) for _ in pts]
    new_pts = [(_[0] + offset_x * i, _[1] + offset_y * i) for _ in pts]
    
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


loop_x = int(lyr_w / (4 * length))
# for _ in xrange(int(loop_x*1.4)):


arcpy.AddMessage("Start to Ccreate Geometry...")
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

"""--------����Ҫ��------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------ɾ����Χ���Ҫ��------"""

feature_layer = "f_layer"

arcpy.AddMessage("Geometry Created")
try:
    arcpy.MakeFeatureLayer_management(shpfile, feature_layer)
except UnicodeEncodeError:
    arcpy.AddError("\n����ArcMap�汾�ľ��ޣ���ʹ�ô�Ӣ�����·����")
arcpy.SelectLayerByLocation_management(feature_layer,
                                       "INTERSECT", input_fc)
# selection_type="SWITCH_SELECTION"
# arcpy.DeleteFeatures_management(feature_layer)
arcpy.CopyFeatures_management(feature_layer, output_fc)
arcpy.Delete_management(shpfile)
arcpy.AddMessage("Geometry Cliped")
arcpy.AddMessage("Finshed")
"""--------ɾ����Χ���Ҫ��------"""
"""--------------------------------------"""
