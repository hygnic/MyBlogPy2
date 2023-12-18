# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              t22
# Author:            Hygnic
# Created on:        2023/11/5 23:02
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------

import arcpy
# A list of features and coordinate pairs
# feature_info = [[[1, 2], [2, 4], [3, 7]],
#                 [[6, 8], [5, 7], [7, 2], [9, 5]]]


feature_info =[[
    [4,4],[4,6],[6,6],[6,4],[4,4]]
    ,[[2,2],[2,8],[8,8],[8,2],[2,2]]
    ,[[0,0],[0,10],[10,10],[10,0],[0,0]]]
# A list that will hold each of the Polygon objects
features = []
# Create Polygon objects based an the array of points
for feature in feature_info:
    array = arcpy.Array([arcpy.Point(*coords) for coords in feature])
    
    # Add the first coordinate pair to the end to close polygon
    array.append(array[0])
    features.append(arcpy.Polygon(array))
# Persist a copy of the geometry objects using CopyFeatures
arcpy.CopyFeatures_management(features, "D:/polygons.shp")
