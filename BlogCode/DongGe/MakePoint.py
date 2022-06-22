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


Usage:               
"""
# -------------------------------------------
import arcpy
import os

##-------------------SETTING
test_polygon = r"C:\Users\Administrator\Documents\MoveOn\MyBlogPy2\BlogCode\DongGe\testp.shp"
arcpy.env.workspace = os.getcwd()
arcpy.env.overwriteOutput = True


##-------------------PARA
point_name = "pointtttg.shp"

# polyFC = arcpy.GetParameterAsText(0)
# outCentroids = arcpy.GetParameterAsText(1)

polyFC = test_polygon
outCentroids = os.path.join(arcpy.env.workspace,point_name)


##-------------------FUNCTION 创建质心点
# create output file. Add "ORIG_ID" field.
if not arcpy.Exists(test_polygon):
    raise NameError("Input feature do not exists.")
arcpy.CreateFeatureclass_management(os.path.dirname(test_polygon),
                                    point_name,
                                    "POINT",
                                    spatial_reference=test_polygon)
arcpy.AddField_management(outCentroids,'ORIG_ID', 'LONG')

# collect all of the polygon centroids into an array

pointArray = []
for row in arcpy.da.SearchCursor(polyFC, ["SHAPE@",'OID@']):
    rowArray = []
    rowArray.append(row[0].centroid)
    for field in range(1,len(row)):
        rowArray.append(row[field])
    pointArray.append(rowArray)
del row


# write the centroids to the output file
cursor = arcpy.da.InsertCursor(outCentroids, ["SHAPE@",'OID@'])

for point in pointArray:
    arcpy.AddMessage(point)
    cursor.insertRow(point)

del cursor


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
