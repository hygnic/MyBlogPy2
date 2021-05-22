# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code5
# Author:            Hygnic
# Created on:        2021/5/12 20:44
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy

# mxd文档对象
mxd = arcpy.mapping.MapDocument("CURRENT")
# 数据框
df = arcpy.mapping.ListDataFrames(mxd)[0]
lyr_path = ur"G:\MoveOn\arcpyTutoraial\SHP\Boroughs.shp"
lyr = arcpy.mapping.Layer(lyr_path)

arcpy.mapping.AddLayer(df, lyr)

# 刷新 arcmap 界面
arcpy.RefreshTOC()
arcpy.RefreshActiveView()
