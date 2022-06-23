# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              MakePoint
# Author:            Hygnic
# Created on:        2022/6/22 20:12
# Version:           
# Reference:         
"""
Description:
根据面图层打钻井点。点的上下左右都有点，距离为x。
    中心点如何确认？
        面要素的几何中心作为起始中心点

提取面图层的质心

Usage:               
"""
# -------------------------------------------
import arcpy
import os

##-------------------SETTING
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True


##-------------------PARA
# 输入要素类
# polyFC = test_polygon
in_fc = arcpy.GetParameterAsText(0)
# in_fc = r"C:\Users\Administrator\Documents\MoveOn\MyBlogPy2\BlogCode\DongGe\testp.shp"
# 公司路径
# in_fc = r"E:\Document\MoveOn\MyBlogPy2\BlogCode\DongGe\testp.shp"


# 输出质心点要素类
# outCentroids = os.path.join(arcpy.env.workspace,point_name)
outCentroids = arcpy.GetParameterAsText(1)
# point_name = "pointtttg.shp"


##-------------------FUNCTION 创建质心点
# create output file. Add "ORIG_ID" field.
if not arcpy.Exists(in_fc):
    raise NameError("Input feature do not exists.")
arcpy.CreateFeatureclass_management(os.path.dirname(outCentroids),
                                    os.path.basename(outCentroids),
                                    "POINT",
                                    template=in_fc,
                                    spatial_reference=in_fc)

# collect all of the polygon centroids into an array
pointArray = []
for row in arcpy.da.SearchCursor(in_fc, ["SHAPE@","*"]):
    rowArray = []
    rowArray.append(row[0].centroid)
    for field in range(1,len(row)):
        rowArray.append(row[field])
    pointArray.append(rowArray)
del row

# write the centroids to the output file
cursor = arcpy.da.InsertCursor(outCentroids, ["SHAPE@","*"])

for point in pointArray:
    arcpy.AddMessage(point)
    cursor.insertRow(point)

del cursor