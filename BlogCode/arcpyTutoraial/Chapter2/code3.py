# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code3
# Author:            Hygnic
# Created on:        2021/5/12 16:07
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
# 使用Layer类
shp_file = arcpy.mapping.Layer("../SHP/Boroughs.shp")
arcpy.CopyFeatures_management(shp_file, "out3.shp")
# ▶注释1◀
shp_file2 = arcpy.mapping.Layer("../NYC.gdb/Boroughs")