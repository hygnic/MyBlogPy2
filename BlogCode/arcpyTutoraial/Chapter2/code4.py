# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              code4
# Author:            Hygnic
# Created on:        2021/5/12 16:30
# Version:           ArcGIS10.3 Python 2.7.8
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os

class CAD2Shp(object):
    def __init__(self, cad):
        self.cad = cad
        self.convert()
    
    
    def convert(self):
        pt = arcpy.mapping.Layer(self.cad+"\Point")
        pl = arcpy.mapping.Layer(self.cad+"\Polyline")
        pg = arcpy.mapping.Layer(self.cad+"\Polygon")
        arcpy.CopyFeatures_management(pt, "pt.shp")
        arcpy.CopyFeatures_management(pl, "er")
        arcpy.CopyFeatures_management(pg, "pg")


if __name__ == '__main__':
    arcpy.env.workspace = os.getcwd()
    arcpy.env.overwriteOutput = True
    CAD2Shp(u"设计图.dwg")