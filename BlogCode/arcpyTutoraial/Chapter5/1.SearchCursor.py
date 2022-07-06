# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code3
# Author:            Hygnic
# Created on:        2021/6/2 18:51
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

field = ["BoroName", "SHAPE@AREA"] # ▶注释1◀
with arcpy.da.SearchCursor("Boroughs", field) as cursor:
    print cursor.fields
    print "Next 1: {}".format(cursor.next()) # ▶注释2◀
    print "Next 2: {}".format(cursor.next())
    print "Next 3: {}".format(cursor.next())
    print "Next 4: {}".format(cursor.next())
    print "Next 5: {}".format(cursor.next())
    cursor.reset() # ▶注释3◀
    print "Next 1: {}".format(cursor.next())
    print "Next 2: {}".format(cursor.next())
    print "Next 3: {}".format(cursor.next())
    print "Next 4: {}".format(cursor.next())
    print "Next 5: {}".format(next(cursor)) # ▶注释4◀



