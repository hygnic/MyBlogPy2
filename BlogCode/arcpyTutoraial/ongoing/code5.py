# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code4
# Author:            Hygnic
# Created on:        2021/5/16 15:48
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

# mxd = arcpy.mapping.MapDocument("../MXD/mxd1 - copy.mxd")
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
lyr = arcpy.mapping.ListLayers(mxd, data_frame=df)[0]

full_path = r"/Misc/style.style"
style_item = arcpy.mapping.ListStyleItems(full_path, "Fill Symbols", "green*")[0]
legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]

legend.updateItem(lyr, style_item)
arcpy.RefreshTOC()
arcpy.RefreshActiveView()