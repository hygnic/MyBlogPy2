# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              3.InsertCursor
# Author:            Hygnic
# Created on:        2021/7/13 20:25
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
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

field = ["BoroName", "SHAPE@"]
cursor = arcpy.da.InsertCursor("Boroughs", field)

array = arcpy.Array([arcpy.Point(993701.189, 232208.219),
                     arcpy.Point(976940.744, 245402.664),
                     arcpy.Point(965482.411, 211027.664),
                     arcpy.Point(974162.966, 191583.219)])
new_polygone = arcpy.Polygon(array) # ▶注释1◀

cursor.insertRow(["test", new_polygone]) # ▶注释2◀
cursor.insertRow(["test2", None]) # ▶注释3◀
del cursor