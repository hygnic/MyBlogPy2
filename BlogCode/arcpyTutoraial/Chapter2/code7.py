# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code7
# Author:            Hygnic
# Created on:        2021/5/13 14:00
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os

cws = os.getcwd()
# 设置工作空间
arcpy.env.workspace = cws
# 可以覆盖同名文件
arcpy.env.overwriteOutput = True

raster_p = "../Raster/N31E107.tif"
# ▶注释1◀
new_raster = arcpy.sa.Slope(raster_p)
# ▶注释2◀
new_raster.save("../NYC.gdb/raster")
new_raster.save("raster.tif")

# ▶注释3◀
raster_obj = arcpy.Raster(raster_p)
arcpy.sa.Slope(raster_obj).save("raster2.tif")