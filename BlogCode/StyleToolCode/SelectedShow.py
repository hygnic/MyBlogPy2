# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              SelectedShow
# Author:            Hygnic
# Created on:        2022/7/5 15:53
# Version:           
# Reference:         
"""
Description:         突出显示效果
消除面部件获得一个图层
然后在内容列表复制该图层，数据未复制
在图层a的基础上定义查询，
#TODO 如果我单独选择几个要素运行工具会怎样呢？
Usage:               
"""
# -------------------------------------------
import arcpy
import os
from random import randint


#>>>>>>>>>>>>>>>>>Function>>>>>>>>>>>>>>>>>>>>>>>

def show_selected_feature(layer_in, where, layer_out):
    arcpy.env.workspace = os.path.basename(layer_out)
    
    layer_in = arcpy.mapping.Layer(layer_in)
    # eliminte_layer = "%scratchGDB%/layer{}".format(randint(0,10000))
    arcpy.EliminatePolygonPart_management(layer_in,
                                          layer_out,
                                          "AREA",
                                          90000000000,
                                          part_option="CONTAINED_ONLY" )
    
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = mxd.activeDataFrame
    out_layer_feature = "out_layer_feature"
    arcpy.MakeFeatureLayer_management(layer_out, out_layer_feature)
    
    
    
if __name__ == '__main__':
    #>>>>>>>>>>>>>>>>>Input Para>>>>>>>>>>>>>>>>>>>>>>>
    in_layer = arcpy.GetParameterAsText(0)
    sql_express = arcpy.GetParameterAsText(1)
    out_layer = arcpy.GetParameterAsText(2)
    
    #>>>>>>>>>>>>>>>>>Env Setting>>>>>>>>>>>>>>>>>>>>>>>
    # arcpy.env.workspace = os.path.basename(out_layer)

    # argv = tuple(arcpy.GetParameterAsText(i)
    #                  for i in range(arcpy.GetArgumentCount()))
    
    arcpy.AddMessage(sql_express)
    show_selected_feature(in_layer, sql_express, out_layer)