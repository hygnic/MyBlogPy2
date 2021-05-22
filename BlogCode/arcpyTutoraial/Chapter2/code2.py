# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code1
# Author:            Hygnic
# Created on:        2021/5/12 11:10
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

# 导出数据库要素类 ▶注释1◀
arcpy.CopyFeatures_management("../NYC.gdb/Boroughs", "out2.shp")
# 将shp文件导入数据库 ▶注释2◀
arcpy.CopyFeatures_management("../SHP/Boroughs.shp",
                              "../NYC.gdb/Boroughs2")
