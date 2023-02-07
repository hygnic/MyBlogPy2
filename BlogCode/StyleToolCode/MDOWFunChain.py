# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              MODW
# Author:            Hygnic
# Created on:        2022/7/8 21:51
# Version:           
# Reference:         
"""
Description:         使用简单的函数链创建多向山体阴影
                1.复制需要制作山体阴影的DEM一份，不然会改变原始 DEM
                2.应用函数链到复制的DEM
                3.添加到 MXD 中
Usage:               
"""
# -------------------------------------------
import os
import arcpy
import sys




def apply_mdow(inraster, outraster):
    wksp = os.path.dirname(outraster)
    arcpy.env.workspace = wksp
    
    toolbox = os.path.abspath(sys.argv[0])
    #@@ 未导入工具箱时
    
    # tool_dir = os.path.abspath(os.path.join(os.path.dirname(toolbox), "StyleTool"))
    #@@ Run in toolbox
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # lyr
    dir_rasterfunction = os.path.join(tool_dir, "RasterFunction")
    
    function_clain = os.path.join(dir_rasterfunction, "MDOW.rft.xml")
    
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
    in_raster = arcpy.GetParameterAsText(0)
    out_raster = arcpy.GetParameterAsText(1)

    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ------")
    arcpy.AddMessage("|---------------------------------|\n")
    apply_mdow(in_raster, out_raster)