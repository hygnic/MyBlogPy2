# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code4
# Author:            Hygnic
# Created on:        2021/5/16 15:48
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         需要在 Python 窗口中运行
Usage:               
"""
# -------------------------------------------
from __future__ import unicode_literals
import arcpy
import os

cws = os.getcwd()
arcpy.env.workspace = cws
arcpy.env.overwriteOutput = True

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
lyr = arcpy.mapping.ListLayers(mxd, data_frame=df)[0]

# 设置定义查询语句 ▶注释1◀
# lyr.visible = True
# express = "BoroName = 'Bronx'"
# lyr.definitionQuery = express

# 设置标注查询语句
lyr.showLabels = True
if lyr.supports("LABELCLASSES"):
    for lblClass in lyr.labelClasses:
        lblClass.expression = "[BoroName]" # ▶注释2◀
        lblClass.SQLQuery = "Shape_Length >= 700000" # ▶注释3◀
        lblClass.showClassLabels = True
        print lblClass.className

arcpy.RefreshTOC()
arcpy.RefreshActiveView()
