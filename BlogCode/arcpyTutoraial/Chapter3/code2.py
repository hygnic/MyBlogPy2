# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code2
# Author:            Hygnic
# Created on:        2021/5/14 17:44
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

mxd = arcpy.mapping.MapDocument("../MXD/mxd1.mxd")
# mxd = arcpy.mapping.MapDocument("CURRENT")

df = arcpy.mapping.ListDataFrames(mxd)[0]

df.displayUnits = "Meters"

print "displayUnits: {}".format(df.displayUnits)
print "mapUnits: {}".format(df.mapUnits)
print "elementHeight: {}".format(df.elementHeight)
print "elementWidth: {}".format(df.elementWidth)
print "elementPositionX: {}".format(df.elementPositionX)
print "elementPositionY: {}".format(df.elementPositionY)
print "referenceScale: {}".format(df.referenceScale)
print "type: {}".format(df.type)
print "scale: {}".format(df.scale)
print "extent: {}".format(df.extent)
print "spatialReference: {}".format(df.spatialReference)
print "description: {}".format(df.description)
print "name: {}".format(df.name)
print "credits: {}".format(df.credits)


df.zoomToSelectedFeatures ()
mxd.saveACopy("../MXD/mxd1 - copy.mxd", version="10.1")

# arcpy.RefreshTOC()
# arcpy.RefreshActiveView()#