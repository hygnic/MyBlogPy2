# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              IlluminatedContours
# Author:            Hygnic
# Created on:        2023/2/2 15:23
# Version:           
# Reference:
# illumContours.py
# This technique is an implementation of the Tanaka method developed:
# by Patrick Kennelly and used with permission.
# Programmed by Linda Beale, Esri Inc
#
# Description:
# Tanaka referred to his technique as the relief contour method, although
# it is typically referred to as the illuminated contour or Tanaka method.
"""
Description:         Illuminated Contours 明暗等值线
Usage:               
"""
# -------------------------------------------
import os
import sys
import arcpy
from arcpy import env
from arcpy.sa import *

def illuminatedContours(inDEM, contourWidth, outFC, baseContour, zFactor, altitude, azimuth, lowversion):
    """
    illuminatedContours: calculates illuminated contours

    Required arguments:
    Inputs:
        inDEM -- Input DEM.
        contourWidth -- contour width.
        baseContour -- base contour value.
        zFactor -- z value.
    Outputs:
        outFC -- output Feature Class.
    """
    try:
        arcpy.env.overwriteOutput = True
        # Check out the Spatial Analyst license
        arcpy.CheckOutExtension("Spatial")
        
        # Define the env workspace
        outPath = os.path.dirname(outFC)
        env.workspace = outPath
        
        # Inputs
        altitude = altitude #45
        azimuth = azimuth #315
        
        # Outputs
        reclassPoly = arcpy.CreateFeatureclass_management("in_memory", "reclassPoly")
        outContours = arcpy.CreateFeatureclass_management(outPath, "outContours")
        
        # Process: Hillshade
        outHillshade = Hillshade(inDEM, azimuth, altitude, "NO_SHADOWS", zFactor)
        hillshadeCalc = (ACos(Float(outHillshade) / 255)) * 57.2958
        
        # Process: Reclassify
        remapRange = RemapRange([   [5.0758605003356934, 9.6565171082814523,1], [9.6565171082814523, 14.237173716227211,2],
                                    [14.237173716227211, 18.81783032417297,3], [18.81783032417297, 23.398486932118729,4],
                                    [23.398486932118729, 27.979143540064488,5], [27.979143540064488, 32.559800148010247,6],
                                    [32.559800148010247, 37.140456755956009,7], [37.140456755956009, 41.721113363901772,8],
                                    [41.721113363901772, 46.301769971847534,9], [46.301769971847534, 50.882426579793297,10],
                                    [50.882426579793297, 55.463083187739059,11], [55.463083187739059, 60.043739795684822,12],
                                    [60.043739795684822, 64.624396403630584,13], [64.624396403630584, 69.205053011576339,14],
                                    [69.205053011576339, 73.785709619522095,15], [73.785709619522095, 78.36636622746785,16],
                                    [78.36636622746785, 82.947022835413605,17], [82.947022835413605, 87.527679443359375,18]])
        outReclass = Reclassify(hillshadeCalc, "Value", remapRange)
        
        # Process: Create contours
        arcpy.RasterToPolygon_conversion(outReclass, reclassPoly, "SIMPLIFY", "VALUE")
        Contour(inDEM, outContours, contourWidth, baseContour, zFactor)
        inFeatures = [outContours, reclassPoly]
        arcpy.Intersect_analysis(inFeatures, outFC)
        
        # set the symbology
        # toolLayerPath = dir_lyr
        # lyrFile = os.path.join(toolLayerPath, "Illuminated Contours.lyr")
        # params = arcpy.GetParameterInfo()
        # params[2].symbology = lyrFile
        
        # Process: Delete temp features0
        arcpy.Delete_management(outContours)
        
        
    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages(2))
# End main function

def modify(lowversion):
    # 添加组；将生成的 Contours 添加到组中；将 inDEM 以特定的样式添加到组中
    # Add layers to group - 10x.
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = mxd.activeDataFrame
    
    lyr_contours = arcpy.mapping.Layer(arcpy.GetParameterAsText(2))
    # 确保添加的图层名称和用户输入的一致
    layer_name = os.path.basename(arcpy.GetParameterAsText(2))
    # layer_contours = arcpy.MakeFeatureLayer_management(lyr_contours, layer_name)
    layer_dem = arcpy.MakeRasterLayer_management(arcpy.GetParameterAsText(0), "layer_dem")
    
    lyr1 = os.path.join(dir_lyr, "Illuminated_Contour.lyr")
    # arcpy.AddMessage(lowversion)
    # 低版本适配选项，Illuminated Contours101.lyr 是使用 ArcMap10.1保存的lyr文件
    if lowversion == "true":
        lyr2 = os.path.join(dir_lyr, "Illuminated Contours101.lyr")
    else:
        lyr2 = os.path.join(dir_lyr, "Illuminated Contours1082.lyr")
    lyr3 = os.path.join(dir_lyr, "IllumContou_dem.lyr")
    # arcpy.ApplySymbologyFromLayer_management(lyr_contours, lyr2) #TODO 会报错
    arcpy.ApplySymbologyFromLayer_management(layer_dem, lyr3)
    
    
    # Add layers to group - 10x.
    groupLayer = arcpy.mapping.Layer(lyr1)
    arcpy.mapping.AddLayer(df, groupLayer, "TOP")
    groupLayer = arcpy.mapping.ListLayers(mxd, "Illuminated_Contour", df)[0]
    arcpy.mapping.AddLayerToGroup(df, groupLayer, lyr_contours, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, groupLayer, layer_dem.getOutput(0), "BOTTOM")
    
    # 由于使用ApplySymbologyFromLayer_management方法会报错，
    # 所以使用 UpdateLayer 方法，
    # 且必须使用arcpy.mapping.Layer方法处理 lyr 文件
    layer_c2 = arcpy.mapping.ListLayers(mxd, layer_name, df)[0]
    lyr2 = arcpy.mapping.Layer(lyr2)
    arcpy.mapping.UpdateLayer(df, layer_c2, lyr2)

    del mxd, df


if __name__ == '__main__':
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ----- ")
    arcpy.AddMessage(" ---- 参考 by Kenneth Field (Esri) --- ")
    arcpy.AddMessage(" ---- 技术 by Linda Beale (Esri) ----- ")
    arcpy.AddMessage("|---------------------------------|\n")
    
    
    # Get Toolbox path
    toolbox = os.path.abspath(sys.argv[0])
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    dir_lyr = os.path.join(tool_dir, "lyr")
    
    
    args = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))
    illuminatedContours(*args)
    modify(arcpy.GetParameterAsText(7))

