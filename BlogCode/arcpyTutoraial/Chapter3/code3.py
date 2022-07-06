# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code3
# Author:            Hygnic
# Created on:        2021/5/15 18:49
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
from __future__ import unicode_literals
import arcpy
import os

cws = os.getcwd()
arcpy.env.workspace = cws
arcpy.env.overwriteOutput = True

lyr = arcpy.mapping.Layer("../SHP/Boroughs.shp")
print "Before:{}".format(lyr.getSelectionSet()) # ▶注释1◀

arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "")
lyr_id = lyr.getSelectionSet()
print "After Selected:{}".format(lyr_id) # ▶注释2◀

new_id = lyr_id[:3]
print "New ID:{}".format(new_id)
lyr.setSelectionSet("NEW", new_id) # ▶注释3◀

arcpy.CopyFeatures_management(lyr, "newID_lyr.shp") # ▶注释4◀