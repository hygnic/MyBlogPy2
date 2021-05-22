# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code6
# Author:            Hygnic
# Created on:        2021/5/12 22:12
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy

arcpy.env.overwriteOutput = True

# mxd文档对象
mxd = arcpy.mapping.MapDocument("chapter2MXD.mxd")
# 数据框 ▶注释1◀
df = arcpy.mapping.ListDataFrames(mxd)[0]
# ▶注释2◀
print "DataFrame Scale:{}".format(df.scale)
print "DataFrame Extent:{}".format(df.extent)
print "DataFrame Type:{}".format(df.type)

# ▶注释3◀
exist_lyr = arcpy.mapping.ListLayers(mxd)[0]
print exist_lyr.name

# 添加shp到mxd ▶注释4◀
lyr_path = ur"../SHP/Boroughs.shp"
lyr = arcpy.mapping.Layer(lyr_path)
arcpy.mapping.AddLayer(df, lyr)
# 添加栅格数据 ▶注释5◀
raster_p = "../Raster/N31E107.tif"
raster_lyr = arcpy.mapping.Layer(raster_p)
arcpy.mapping.AddLayer(df, raster_lyr)

# ▶注释6◀
mxd.saveACopy("output.mxd", version="10.1")