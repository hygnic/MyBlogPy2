# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              TwoDirctionalHS
# Author:            Hygnic
# Created on:        2022/4/9 21:09
# Version:           
# Reference:         
"""
Description:         多向Hillshade
Usage:               
"""
# -------------------------------------------
import os
import arcpy
from random import randint


def multip_direction_hillshade(raster_layer, z_factor, altitude, output):
    
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    z_factor = float(z_factor)
    altitude = int(altitude)

    # Process: Hillshade (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster = "%scratchFolder%/" + raster_name
    Hillshade = Output_raster
    Output_raster = arcpy.sa.Hillshade(in_raster=raster_layer,
                                       azimuth=315,altitude=altitude,
                                       model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster.save(Hillshade)


    # Process: Hillshade (2) (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster_2_ = "%scratchFolder%/" + raster_name
    Hillshade_2_ = Output_raster_2_
    Output_raster_2_ = arcpy.sa.Hillshade(in_raster=raster_layer,
                                          azimuth=0, altitude=altitude,
                                          model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster_2_.save(Hillshade_2_)


    # Process: Hillshade (3) (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster_3_ = "%scratchFolder%/" + raster_name
    Hillshade_3_ = Output_raster_3_
    Output_raster_3_ = arcpy.sa.Hillshade(in_raster=raster_layer,
                                          azimuth=45, altitude=altitude,
                                          model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster_3_.save(Hillshade_3_)


    # Process: Hillshade (4) (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster_4_ = "%scratchFolder%/" + raster_name
    Hillshade_4_ = Output_raster_4_
    Output_raster_4_ = arcpy.sa.Hillshade(in_raster=raster_layer,
                                          azimuth=90, altitude=altitude,
                                          model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster_4_.save(Hillshade_4_)


    # Process: Hillshade (5 (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster_5_ = "%scratchFolder%/" + raster_name
    Hillshade_5_ = Output_raster_5_
    Output_raster_5_ = arcpy.sa.Hillshade(in_raster=raster_layer,
                                          azimuth=135, altitude=altitude,
                                          model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster_5_.save(Hillshade_5_)


    # Process: Hillshade (6) (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster_6_ = "%scratchFolder%/" + raster_name
    Hillshade_6_ = Output_raster_6_
    Output_raster_6_ = arcpy.sa.Hillshade(in_raster=raster_layer,
                                          azimuth=180, altitude=altitude,
                                          model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster_6_.save(Hillshade_6_)

    # Process: Hillshade (7) (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster_7_ = "%scratchFolder%/" + raster_name
    Hillshade_7_ = Output_raster_7_
    Output_raster_7_ = arcpy.sa.Hillshade(in_raster=raster_layer,
                                          azimuth=225, altitude=altitude,
                                          model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster_7_.save(Hillshade_7_)


    # Process: Hillshade (8) (Hillshade) (sa)
    raster_name = "hs_"+str(randint(0,999999))
    Output_raster_8_ = "%scratchFolder%/" + raster_name
    Hillshade_8_ = Output_raster_8_
    Output_raster_8_ = arcpy.sa.Hillshade(in_raster=raster_layer,
                                          azimuth=270, altitude=altitude,
                                          model_shadows="NO_SHADOWS", z_factor=z_factor)
    Output_raster_8_.save(Hillshade_8_)


    # Process: Raster Calculator (Raster Calculator)
    raster_name = "hs_"+str(randint(0,999999))
    Raster_Calculator = "%scratchFolder%/" + raster_name
    rastercalc = (Output_raster +  Output_raster_2_ + Output_raster_3_+
                  Output_raster_4_ + Output_raster_5_+
                  Output_raster_6_+Output_raster_7_+Output_raster_8_)/8
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
    arcpy.Delete_management(Output_raster_3_)
    arcpy.Delete_management(Output_raster_4_)
    arcpy.Delete_management(Output_raster_5_)
    arcpy.Delete_management(Output_raster_6_)
    arcpy.Delete_management(Output_raster_7_)
    arcpy.Delete_management(Output_raster_8_)
    arcpy.Delete_management(Raster_Calculator)


if __name__ == '__main__':
    # Global Environment settings
    # arcpy.env.addOutputsToMap = True
    arcpy.env.workspace = os.path.dirname(arcpy.GetParameterAsText(3))
    work = arcpy.env.workspace
    
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    multip_direction_hillshade(*argv)