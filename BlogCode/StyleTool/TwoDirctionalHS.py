# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              TwoDirctionalHS
# Author:            Hygnic
# Created on:        2022/4/9 21:09
# Version:           
# Reference:         
"""
Description:         双向Hillshade
Usage:               
"""
# -------------------------------------------
import os
import arcpy
from random import randint


def two_direction_hillshade(raster_layer, z_factor, altitude, output, azimuth):
    
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    z_factor = int(z_factor)
    altitude = int(altitude)
    arcpy.AddMessage(azimuth)
    arcpy.AddMessage(type(azimuth))
    if azimuth == u"true":
        arcpy.AddMessage("first")
        azimuth1 = 315
        azimuth2 = 90
    else:
        arcpy.AddMessage("sec")
        azimuth1 = 135
        azimuth2 = 180
        
        
    # Process: Hillshade (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster = "%scratchFolder%/" + raster_name
    Hillshade = Output_raster
    Output_raster = arcpy.sa.Hillshade(in_raster=raster_layer,
                                       azimuth=azimuth1,altitude=altitude,
                                       model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster.save(Hillshade)


    # Process: Hillshade (2) (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster_2_ = "%scratchFolder%/" + raster_name
    Hillshade_2_ = Output_raster_2_
    Output_raster_2_ = arcpy.sa.Hillshade(in_raster=raster_layer,
                                          azimuth=azimuth2, altitude=altitude,
                                          model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster_2_.save(Hillshade_2_)


    # Process: Raster Calculator (Raster Calculator)
    raster_name = "hs_"+str(randint(0,999999))
    Raster_Calculator = "%scratchFolder%/" + raster_name
    rastercalc = (Output_raster +  Output_raster_2_ )/2
    rastercalc.save(Raster_Calculator)
    arcpy.CopyRaster_management(in_raster=Raster_Calculator,
                                out_rasterdataset=output,
                                pixel_type="8_BIT_UNSIGNED")
    
    
    # # Adding Result Raster Layer to Arcmap
    # mxd = arcpy.mapping.MapDocument("CURRENT")
    # # df = arcpy.mapping.ListDataFrames(mxd)
    # df = mxd.activeDataFrame
    # # 为添加到 mxd 中的栅格取名
    # arcpy.AddMessage(os.path.basename(output))
    # raster_lyr = os.path.basename(output)+"_layer" # TODO 直接使用名称无法添加进去 10.6
    # result = arcpy.MakeRasterLayer_management(output, raster_lyr)
    # layer = result.getOutput(0)
    # arcpy.mapping.AddLayer(data_frame=df, add_layer=layer)
    
    
    # Delete Processing Raster File
    arcpy.Delete_management(Output_raster)
    arcpy.Delete_management(Output_raster_2_)
    arcpy.Delete_management(Raster_Calculator)


if __name__ == '__main__':
    # Global Environment settings
    # arcpy.env.addOutputsToMap = True
    arcpy.env.workspace = os.path.dirname(arcpy.GetParameterAsText(3))
    work = arcpy.env.workspace
    
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    two_direction_hillshade(*argv)