#!/usr/bin/env python
# -*- coding:cp936 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2020/4/22 16:44
# Reference:
"""
Description: 浮雕制作工具，构建阴影栅格，设置50%透明度置于图层下
* 已经导入工具箱
arcgis 10.3
Usage:
"""
# ---------------------------------------------------------------------------
import arcpy


def emboss(layer, buffer_distance, out_raster):
    """
    %scratchGDB%
    :param layer: shapefile
    :param buffer_distance: inner buffer distance int -300
    :param out_raster: output raster
    :return: None
    """
    # inner buffer
    in_memory_buffer = "in_memory/buffer02011"
    arcpy.Buffer_analysis(layer, in_memory_buffer, buffer_distance, "FULL",
                          "ROUND", "NONE")
    # distance
    in_memory_euc = "in_memory/euc_distance"
    arcpy.gp.EucDistance_sa(in_memory_buffer, in_memory_euc, "", "", "")
    # clip
    in_memory_clip = "in_memory/clip_raster"
    arcpy.Clip_management(in_memory_euc, "", in_memory_clip, layer, "", True,
                          False)
    arcpy.env.addOutputsToMap = True
    # output_raster = "eds2"
    # hill shadow
    arcpy.gp.HillShade_sa(in_memory_clip, out_raster, "315",
                          "45", "NO_SHADOWS", "1")
    # mxd = arcpy.mapping.MapDocument("CURRENT")
    # df = mxd.activeDataFrame
    # arcpy.mapping.AddLayer(df, arcpy.Raster(out_raster))
    

if __name__ == '__main__':
    
    arcpy.env.overwriteOutput = True
    lyrr_name = arcpy.GetParameterAsText(0)
    arcpy.AddMessage(lyrr_name)  # XJQY5203242019
    arcpy.AddMessage(type(lyrr_name))  # <type 'unicode'>
    input_distance = arcpy.GetParameterAsText(1)
    output_raster = arcpy.GetParameterAsText(2)
    # mxd1 = arcpy.mapping.MapDocument("CURRENT")
    # lyr = arcpy.mapping.ListLayers(mxd1, lyrr_name)[0]
    # make emboss effect
    # 设置处理范围和输出的栅格腌膜范围
    arcpy.env.extent = lyrr_name
    arcpy.env.mask = lyrr_name
    
    emboss(lyrr_name, input_distance, output_raster)
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
