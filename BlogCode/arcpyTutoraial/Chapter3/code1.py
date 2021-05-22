# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code1
# Author:            Hygnic
# Created on:        2021/5/14 16:26
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

print "activeDataFrame:{}".format(mxd.activeDataFrame)
print "activeView:{}".format(mxd.activeView)
print "author:{}".format(mxd.author)
print "credits:{}".format(mxd.credits)
print "dateExported:{}".format(mxd.dateExported)
print "datePrinted:{}".format(mxd.datePrinted)
print "dateSaved:{}".format(mxd.dateSaved)
print "description:{}".format(mxd.description)
print "filePath:{}".format(mxd.filePath)
print "hyperlinkBase:{}".format(mxd.hyperlinkBase)
print "pageSize:{}".format(mxd.pageSize)
print "title:{}".format(mxd.title)
print "tags:{}".format(mxd.tags)
print "summary:{}".format(mxd.summary)
