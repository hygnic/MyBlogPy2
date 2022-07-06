# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              2.UpdateCursor
# Author:            Hygnic
# Created on:        2021/7/13 11:07
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         ArcGIS10.3 Python 2.7.8
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os

arcpy.env.overwriteOutput = True
wk_path = os.path.abspath("../NYC.gdb")
arcpy.env.workspace = wk_path

field = ["BoroName", "SHAPE@AREA"]
with arcpy.da.UpdateCursor("Boroughs", field) as cursor:
    for row in cursor:
        # row[0] = row[0] + "_1" # ▶注释1◀
        row[0] = row[0][:-2]
        cursor.updateRow(row) # ▶注释2◀


        # for name, area in cursor:
    #     print name
    #     print area
#     all_value = list(cursor)
# print all_value