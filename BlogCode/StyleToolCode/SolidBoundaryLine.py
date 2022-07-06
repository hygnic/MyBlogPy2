# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              SolidBoundaryLine
# Author:            Hygnic
# Created on:        2022/7/6 21:55
# Version:           
# Reference:
"""
Description:         立体边界效果>>面图层转换为线图层、制图表达效果、偏移切线
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys
from random import randint


def update_representation(inputfile, rep_lyr, output):
    """
    给图层添加指定的制图表达效果并添加到 ArcMap 中
    :param inputfile: 输入图层
    :param rep_lyr: {String} 制图表达图层名称（.lyr file）
    :param output: 样式输出图层
    :return:
    """
    # check
    if not arcpy.Exists(rep_lyr):
        raise RuntimeError("Representation lyr file not exist.")
    
    ####### mxd file obj
    arcpy.env.overwriteOutput = True
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    
    ###### Change polygon to line
    in_lyr = arcpy.mapping.Layer(inputfile)
    randnum = randint(0, 999999)
    lyr_randname = "%scratchGDB%/lyr_{}".format(randnum)
    arcpy.FeatureToLine_management(in_lyr, lyr_randname)
    
    ####### Create a new layer
    arcpy.CopyFeatures_management(lyr_randname, output)
    new_lyr = arcpy.mapping.Layer(os.path.join(work, output))
    
    ####### Make representation symbol to new layer
    representation_lyr = arcpy.mapping.Layer(rep_lyr)
    arcpy.AddMessage("------------------")
    # representation name
    randnum = randint(0, 999999)
    rp_name = "Rep_{}".format(randnum)
    
    ####### Create Representation
    r_func = arcpy.AddRepresentation_cartography
    r_func(new_lyr, rp_name, import_rule_layer=representation_lyr)
    
    ###### copy transparency value
    opacity = representation_lyr.transparency
    new_lyr.transparency = opacity
    
    #       add new layer to arcmap
    arcpy.SetLayerRepresentation_cartography(new_lyr, rp_name)
    arcpy.mapping.AddLayer(df, new_lyr)
    arcpy.Delete_management(lyr_randname)
    
    arcpy.AddMessage("\n------------------")


def add_background_layer(path_gdb, output):
    """
    :param path_gdb:
    :param output: 使用工具的輸出路勁文件夾
    :return:
    """
    ##### Add backgroud layer and erase
    retangle_world = os.path.join(path_gdb, "FeatureClass_RetangleWorld3857")
    retangle_world = arcpy.mapping.Layer(retangle_world)
    
    randnum = randint(0, 999)
    lyr_name = os.path.join(os.path.dirname(output), "Background{}".format(randnum))
    arcpy.Erase_analysis(retangle_world, lyr_name)
    
    ##### 應用 lyr 樣式並添加圖層到 mxd 中


if __name__ == '__main__':
    #------------------------------
    #------------path--------------
    # 返回工具箱的完整名称
    toolbox = os.path.abspath(sys.argv[0])
    arcpy.AddMessage(toolbox)
    # E:\Document\MoveOn\MyBlogPy2\BlogCode\StyleToolCode\SolidBoundaryLine.py

    #@@ 未导入工具箱中
    
    tool_dir = os.path.abspath(os.path.join(os.path.dirname(toolbox),"StyleTool"))
    #@@ 运行于工具箱中
    
    # tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # lyr
    dir_lyr = os.path.join(tool_dir, "lyr") # StyleTool/lyr
    # 制图表达相关
    representation = os.path.join(tool_dir, "Representation")
    rp_gdb = os.path.join(representation, "rep_base.gdb")
    #------------path--------------
    #------------------------------
    
    #------------------------------
    #----------workspace-----------
    arcpy.env.workspace = os.path.dirname(arcpy.GetParameterAsText(1))
    work = arcpy.env.workspace
    #----------workspace-----------
    #------------------------------
    
    rep_lyrr = os.path.join(representation, "SolidBoundaryLine.lyr")
    update_representation(arcpy.GetParameterAsText(0), rep_lyrr,
                          arcpy.GetParameterAsText(1))
