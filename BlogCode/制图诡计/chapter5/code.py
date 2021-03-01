#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2020/4/21 14:51
# Reference:
"""
Description:
Usage:

"""
# ---------------------------------------------------------------------------
import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
lyr1 = arcpy.mapping.ListLayers(mxd)[0]
sorce_lyr_path = ur"图斑样式.lyr"
sourceLayer = arcpy.mapping.Layer(sorce_lyr_path)

arcpy.mapping.UpdateLayer(df, lyr1, sourceLayer)
arcpy.RefreshActiveView()
arcpy.RefreshTOC()

