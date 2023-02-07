# -*- coding:cp936 -*-
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
from math import sin, radians, pow, sqrt

"""--------------------------------------"""
"""--------基本方法------"""


# def conver_point2polgon(a_list):
#     """将普通的点数据转换成可以制作要素的面"""
#     point_obj = [arcpy.Point(i[0], i[1]) for i in a_list]
#     polygon = arcpy.Polygon(arcpy.Array(point_obj))
#     return polygon

def check_extent(input_layer):
    """
    获取输入图层本身的尺寸
    :param input_layer: 输入图层
    :return: 原点，宽，高
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
    提取其中的一组五边形，再提取每组五边形中的一个点，将其转换为 arcpy.Point 对象，多个
    arcpy.Point 对象转换为  arcpy.Array 对象，然后使用  arcpy.Array 对象创建
    arcpy.Polygon 几何对象，最后将几何对象其插入要素类
    :param array_obj:包含多组五边形的列表
    :param featurecalss: 输出矢量文件
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


"""--------基本方法------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------基本属性------"""
arcpy.AddMessage("\n|---------------------------------|")
arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ------")
arcpy.AddMessage("|---------------------------------|\n")



ws = os.path.abspath(os.getcwd())
arcpy.env.workspace = ws
arcpy.env.overwriteOutput = True

"""--------工具箱接口------"""
"""--------工具箱接口------"""
input_fc = arcpy.GetParameterAsText(0)  # featureclass
output_fc = arcpy.GetParameterAsText(1)  # featureclass
side_length = int(arcpy.GetParameterAsText(2))
num = int(arcpy.GetParameterAsText(3))  # x,y轴扩展倍数

ws = os.path.dirname(output_fc)
fc_name = os.path.basename(output_fc)
# arcpy.env.scratchWorkspace = ws
"""--------工具箱接口------"""
"""--------工具箱接口------"""

# 坐标原点
# lyr_o, lyr_w, lyr_h, sr=check_extent("tiff.tif")
lyr_o, lyr_w, lyr_h, sr = check_extent(input_fc)
print "featureclass width:{}".format(lyr_w)
print "featureclass height:{}".format(lyr_h)
origin = lyr_o
oX = origin[0]
oY = origin[1]
print "origin X:{}".format(oX)
print "origin Y:{}".format(oY)
# 五边形短边长度
# length = 300
length = side_length
# 角度
angle01 = 60

# 垂直距离
leng = length * sin(radians(angle01))  # 300*sin60°

cfm = arcpy.CreateFeatureclass_management
# shpfile = cfm(ws, "PentagonTile", "polygon", spatial_reference=sr)
shpfile = cfm(ws, fc_name + "0012701", "polygon", spatial_reference=sr)

"""--------基本属性------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------基本坐标------"""
# 一组五边形在坐标四个象限内的坐标

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

# 左上方向的偏移距离

offset_x = -length * 3 / 2
offset_y = 5 * leng

# 右下方向的偏移距离

offset_x2 = length * 4.5
offset_y2 = -leng

# ratio = lyr_h/(5*leng)
# new_width = length * 3/2 * ratio
# new_hieght= lyr_h
# distance = sqrt(pow(new_width,2) + pow(new_hieght, 2))
# print new_width
# print new_hieght
# print distance

# y轴方向循环次数

loop_y = int(lyr_h / (6 * leng))
array_pt = []  # 用于存放一整列的五边形
# for i in xrange(int(loop_y*1.6)):
for i in xrange(int(loop_y * num)):
    # 向上偏移距离
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
    # 列表中每一个点递增，增加后再封装成列表
    array_pt2 = []
    for point_list in array_pt:
        
        pointss = [(xx+offset_x2, xy+offset_y2) for xx, xy in point_list]
        array_pt2.append(pointss)
    array_pt = array_pt2

"""--------构建要素------"""
"""--------------------------------------"""

"""--------------------------------------"""
"""--------删除范围外的要素------"""

feature_layer = "f_layer"

arcpy.AddMessage("Geometry Created")
try:
    arcpy.MakeFeatureLayer_management(shpfile, feature_layer)
except UnicodeEncodeError:
    arcpy.AddError("\n由于ArcMap版本的局限，请使用纯英文输出路径！")
arcpy.SelectLayerByLocation_management(feature_layer,
                                       "INTERSECT", input_fc)
# selection_type="SWITCH_SELECTION"
# arcpy.DeleteFeatures_management(feature_layer)
arcpy.CopyFeatures_management(feature_layer, output_fc)
arcpy.Delete_management(shpfile)
arcpy.AddMessage("Geometry Cliped")
arcpy.AddMessage("Finshed")
"""--------删除范围外的要素------"""
"""--------------------------------------"""
