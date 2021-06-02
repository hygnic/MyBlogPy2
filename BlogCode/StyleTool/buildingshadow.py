# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              buildingshadow
# Author:            Hygnic
# Created on:        2021/6/2 11:11
# Version:           
# Reference:         <<建筑阴影>>
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys
from random import randint


#------------------------------
#------------path--------------
#       在导入的情况下
arcpy.AddMessage("CURRENT: {}".format(os.getcwd()))
# CURRENT: C:\Windows\system32

# 返回工具箱的完整名称
toolbox = os.path.abspath(sys.argv[0])
arcpy.AddMessage(toolbox)

tool_dir = os.path.abspath(os.path.dirname(toolbox))
# lyr
dir_lyr = os.path.join(tool_dir, "lyr") # StyleTool/lyr
# 制图表达相关
representation = os.path.join(tool_dir, "Representation")
rp_gdb = os.path.join(representation, "rep_base.gdb")
#------------path--------------
#------------------------------

#------------------------------
#----------workspace-----------
os.chdir(tool_dir)
gdb = "workspace.gdb"
if not arcpy.Exists(gdb):
    arcpy.CreateFileGDB_management(os.getcwd(), gdb)
arcpy.env.workspace = os.path.abspath(gdb)
work = arcpy.env.workspace
#----------workspace-----------
#------------------------------

def update_representation(inputfile, rep_lyr, opacity):
    """
    给图层添加指定的制图表达效果并添加到 ArcMap 中
    :param inputfile: 输入图层
    :param rep_lyr: {String} 制图表达图层名称（.lyr file）
    :return:
    """
    #       check
    if not arcpy.Exists(rep_lyr):
        raise RuntimeError("Representation lyr file not exist.")
    
    
    #       mxd file obj
    arcpy.env.overwriteOutput = True
    randnum = randint(0, 999999)
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    
    #       create a new layer
    in_lyr = arcpy.mapping.Layer(inputfile)
    # layer name
    new_n = "{}_{}".format("building", randnum)
    arcpy.CopyFeatures_management(inputfile, new_n)
    # arcpy.AddMessage(type(new_n)) # <'str'>
    # new_lyr = arcpy.mapping.Layer(new_n)
    new_lyr = arcpy.mapping.Layer(os.path.join(work, new_n))
    
    #       make representation symbol to new layer
    representation_lyr = arcpy.mapping.Layer(rep_lyr)
    arcpy.AddMessage("------------------")
    # representation name
    rp_name = "Rep_{}".format(randnum)
    # 创建制图表达
    r_func = arcpy.AddRepresentation_cartography
    r_func(new_lyr, rp_name, import_rule_layer=representation_lyr)
    
    #       add new layer to arcmap
    arcpy.SetLayerRepresentation_cartography(new_lyr, rp_name)
    new_lyr.transparency = int(opacity)
    arcpy.AddMessage(new_lyr.dataSource)
    arcpy.mapping.AddLayer(df, new_lyr)
    arcpy.AddMessage("\n------------------")


if __name__ == '__main__':
    rep_lyrr = os.path.join(representation, "buildingshadow.lyr")
    update_representation(arcpy.GetParameterAsText(0), rep_lyrr,
                          arcpy.GetParameterAsText(1))