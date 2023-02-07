# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              立体要素 3D Choropleth 3D
# Author:            Hygnic
# Created on:        2023/2/1 13:32
# Version:           
# Reference:         
"""
Description:
# This technique was developed by Wes Jones, Esri Inc
#
# Programmed by Linda Beale, Esri Inc
#
# Description: Creates a 3D visualization of a feature class
Usage:               
"""

import os
import sys
import arcpy
from arcpy.sa import *

# Get Toolbox path
toolbox = os.path.abspath(sys.argv[0])
tool_dir = os.path.abspath(os.path.dirname(toolbox))
# Get style lyr path # StyleTool/lyr
dir_lyr = os.path.join(tool_dir, "lyr")


# def symbology(outName1, outName2, outName3):
#     scriptPath = sys.path[0]
#     # one_folder_up = os.path.dirname(scriptPath)
#     # toolLayerPath = os.path.join(one_folder_up, "LayerFiles")
#     toolLayerPath = dir_lyr
#     lyrFile = os.path.join(toolLayerPath, "3DChoro_hardlong.lyr")
#     lyrFile1 = os.path.join(toolLayerPath, "3DChoro_hardshort.lyr")
#     lyrFile2 = os.path.join(toolLayerPath, "3DChoro_soft.lyr")


def GetShadowLength(x):
    if x < 100.0:
        return 100.0
    # arcpy.AddMessage("Test1") TODO
    return math.pow(10.0,-math.log10(x)+3.0)


def Choropleth3D(inFeatures, elevation, outWorkpace, shortName, mediumName, longName, exag, cellSize):
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = outWorkpace
    arcpy.env.mask = inFeatures
    # arcpy.AddMessage("arcpy.env.workspace: {}".format(outWorkpace))
    # arcpy.env.workspace: C:\Users\hygnic\Documents\ArcGIS\newnew.gdb
    
    # Check out the Spatial Analyst license
    arcpy.CheckOutExtension("Spatial")
    
    # Get the shadow lengths
    arr = arcpy.da.FeatureClassToNumPyArray(inFeatures, [elevation])
    try:
        x = arr[elevation].max()
    except ValueError:
        arcpy.AddError("不支持中文字段名，请使用英文字段名")
    # TODO 和numpy有关系，现无法解决。
    # finally:
        # elevation = elevation.encode("cp936")
        # elevation = elevation.encode("utf8")
        # elevation = elevation.decode("cp936")
        # elevation = elevation.decode("utf8")
        x = arr[elevation].max()
    y = GetShadowLength(x)
    
    # Inputs
    longShadow = y * int(exag)
    mediumShadow = y * int(exag) / 2
    shortShadow = y * int(exag) / 4
    
    # Process: Convert to raster
    # conver shp to raster, and create Hillshade
    choroRas = os.path.join(outWorkpace, "choroRas")
    if cellSize == "MAXOF":
        arcpy.FeatureToRaster_conversion(inFeatures, elevation, choroRas)
    else:
        arcpy.FeatureToRaster_conversion(inFeatures, elevation, choroRas, cellSize)
    
    # Process: Hillshade (short shadow)
    arcpy.AddMessage("\n生成阴影……")
    outHillShade1 = Hillshade(choroRas, 315, 45, "SHADOWS", shortShadow)
    attExtract1 = ExtractByAttributes(outHillShade1, "\"VALUE\" =0")
    attExtract1.save(os.path.join(outWorkpace, shortName))
    arcpy.BuildPyramidsandStatistics_management(attExtract1)
    
    # Process: Hillshade (medium shadow)
    # arcpy.AddMessage("\n生成中阴影……")
    outHillShade2 = Hillshade(choroRas, 315, 15, "SHADOWS", mediumShadow)
    attExtract2 = ExtractByAttributes(outHillShade2, "VALUE = 0")
    attExtract2.save(os.path.join(outWorkpace, mediumName))
    arcpy.BuildPyramidsandStatistics_management(attExtract2)

    # Process: Hillshade (long shadow)
    # arcpy.AddMessage("\n生成长阴影……")
    outHillShade3 = Hillshade(choroRas, 315, 15, "SHADOWS", longShadow)
    focalStats = FocalStatistics(outHillShade3, "Rectangle 3 3 CELL", "MEAN", "DATA")
    # sys.exit(1) TODO 这一步会自动生成一个随机名称栅格，未解决
    
    focalStats.save(os.path.join(outWorkpace, longName))
    arcpy.BuildPyramidsandStatistics_management(focalStats)
    
    lyr1 = arcpy.MakeRasterLayer_management(attExtract1, 'short_lyr')
    lyr2 = arcpy.MakeRasterLayer_management(attExtract2, 'medium_lyr')
    lyr3 = arcpy.MakeRasterLayer_management(focalStats, 'long_lyr')
    inlyr = arcpy.MakeFeatureLayer_management(inFeatures, inFeatures+"_lyr")

    
    # Set the symbology
    # 使用的 ApplySymbologyFromLayer_management 方法而不是 updatelayer
    # symbology(outName1, outName2, outName3)
    # create a styled lyr file to inputfeature
    # tempLyr = "%scratchFolder%/temp.lyr"
    # arcpy.SaveToLayerFile_management(inlyr, tempLyr)
    toolLayerPath = dir_lyr

    lyrFile = os.path.join(toolLayerPath, "3DChoro_hardshort.lyr")
    lyrFile1 = os.path.join(toolLayerPath, "3DChoro_hardlong.lyr")
    lyrFile2 = os.path.join(toolLayerPath, "3DChoro_soft.lyr")
    # featureclass styled
    # lyrFeature = os.path.join(toolLayerPath, "3DChoro_feature.lyr")
    group_lyr = os.path.join(toolLayerPath, "3D_Choropleth.lyr")
    
    
    if arcpy.GetInstallInfo()["ProductName"] == "ArcGISPro":
        # Add layers to group - Pro.
        aprx = arcpy.mp.ArcGISProject('CURRENT')
        mp = aprx.listMaps('Map')[0]
        groupLayer = arcpy.mp.LayerFile(group_lyr)
        group_layer = mp.addLayer(groupLayer, "TOP")
        groupLayer = mp.listLayers('3D_Choropleth')[0]
        # arcpy.ApplySymbologyFromLayer_management(inlyr,"tempLyr")
        # arcpy.ApplySymbologyFromLayer_management(inlyr,lyrFeature)
        arcpy.ApplySymbologyFromLayer_management(lyr1, lyrFile)
        arcpy.ApplySymbologyFromLayer_management(lyr2, lyrFile1)
        arcpy.ApplySymbologyFromLayer_management(lyr3, lyrFile2)
        mp.addLayerToGroup(groupLayer, lyr1.getOutput(0), "TOP")
        mp.addLayerToGroup(groupLayer, inlyr.getOutput(0), "BOTTOM")
        translayer = m.listLayers(aprx,"",mp)[2]
        translayer.transparency = 20
        mp.addLayerToGroup(groupLayer, mediumName.getOutput(0), "BOTTOM")
        mp.addLayerToGroup(groupLayer, longName.getOutput(0), "BOTTOM")
        
        del aprx, mp
    else:
        # Add layers to group - 10x.
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        groupLayer = arcpy.mapping.Layer(group_lyr)
        # Add Group layer:3D Choropleth
        arcpy.mapping.AddLayer(df, groupLayer, "TOP")
        groupLayer = arcpy.mapping.ListLayers(mxd, "3D_Choropleth", df)[0]
        #arcpy.ApplySymbologyFromLayer_management(inlyr, inlyrFile)
        # arcpy.ApplySymbologyFromLayer_management(inlyr, tempLyr)
        arcpy.ApplySymbologyFromLayer_management(lyr1, lyrFile)
        arcpy.ApplySymbologyFromLayer_management(lyr2, lyrFile1)
        arcpy.ApplySymbologyFromLayer_management(lyr3, lyrFile2)
        arcpy.mapping.AddLayerToGroup(df, groupLayer, lyr1.getOutput(0), "TOP")
        arcpy.mapping.AddLayerToGroup(df, groupLayer, inlyr.getOutput(0), "BOTTOM")
        translayer = arcpy.mapping.ListLayers(mxd,"",df)[2]
        translayer.transparency = 20
        arcpy.mapping.AddLayerToGroup(df, groupLayer, lyr2.getOutput(0), "BOTTOM")
        arcpy.mapping.AddLayerToGroup(df, groupLayer, lyr3.getOutput(0), "BOTTOM")
        
        del mxd, df
    
    # Process: Delete
    arcpy.Delete_management(choroRas, "")
    arcpy.Delete_management(outHillShade1, "")
    arcpy.Delete_management(outHillShade2, "")
    arcpy.Delete_management(outHillShade3, "")


# End main function

if __name__ == '__main__':
    
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ------")
    arcpy.AddMessage(" --- 参考 by Linda Beale, Esri Inc ---")
    arcpy.AddMessage(" ---- 技术 by Wes Jones, Esri Inc ----")
    arcpy.AddMessage("|---------------------------------|\n")

    args = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))
    Choropleth3D(*args)
