# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              BlurFunChain
# Author:            Hygnic
# Created on:        2023/2/3 17:23
# Version:           
# Reference:         
"""
Description:         栅格模糊效果 使用函数链模板
Usage:               
"""
# -------------------------------------------
import os
import arcpy
import sys

def apply_blur(inraster, outraster, blur):
    wksp = os.path.dirname(outraster)
    arcpy.env.workspace = wksp
    
    toolbox = os.path.abspath(sys.argv[0])
    #@@ 未导入工具箱时
    # tool_dir = os.path.abspath(os.path.join(os.path.dirname(toolbox), "StyleTool"))
    #@@ Run in toolbox
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # Get rasterfunction folder
    dir_rasterfunction = os.path.join(tool_dir, "RasterFunction")
    blur = int(blur)
    if blur == 1:
        blur_filename = "Blur1-2.rft.xml"
    elif blur == 2:
        blur_filename = "Blur2-4.rft.xml"
    elif blur == 3:
        blur_filename = "Blur3-6.rft.xml"
    elif blur == 4:
        blur_filename = "Blur4-9.rft.xml"
    else:
        blur_filename = "Blur5-15.rft.xml"
        
    function_clain = os.path.join(dir_rasterfunction, blur_filename)
    
    # Copy a DEM raster
    DEM_name = arcpy.CreateScratchName(prefix="DEM", workspace=wksp)
    arcpy.CopyRaster_management(inraster, DEM_name)
    raster_lyr = "raster_lyr"
    arcpy.MakeRasterLayer_management(DEM_name, raster_lyr)
    out = arcpy.EditRasterFunction_management(raster_lyr, edit_options="REPLACE",
                                              function_chain_definition=function_clain)
    
    arcpy.env.addOutputsToMap = True
    arcpy.CopyRaster_management(out, outraster)
    # arcpy.AddMessage(outraster)
    
    arcpy.Delete_management(DEM_name)
    arcpy.AddMessage("Done\n")


if __name__ == '__main__':
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ------")
    arcpy.AddMessage("|---------------------------------|\n")
    
    args = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))
    apply_blur(*args)