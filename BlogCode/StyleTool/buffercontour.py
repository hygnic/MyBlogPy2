# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              test_toolbox
# Author:            Hygnic
# Created on:        2021/5/28 11:14
# Version:           
# Reference:         
"""
Description:         <<缓冲区轮廓>>
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys


# 返回工具箱的完整名称
toolbox = os.path.abspath(sys.argv[0])
# arcpy.AddMessage(toolbox)
# G:\MoveOn\Gispot\gispot\StyleTool\StyleTool\StyleToolBox.tbx

#       Setting
tool_dir = os.path.abspath(os.path.dirname(toolbox))
lyr_path = os.path.join(tool_dir, "lyr")
# arcpy.env.scratchWorkspace = tool_dir

os.chdir(tool_dir)
gdb = "workspace.gdb"
if not arcpy.Exists(gdb):
    arcpy.CreateFileGDB_management(os.getcwd(), gdb)
arcpy.env.workspace = os.path.abspath(gdb)
work = arcpy.env.workspace


def make_buffer_ring(inputfile, num):
    
    num = int(num)
    distance = [30*num, 60*num, 90*num]
    name = arcpy.CreateScratchName("buffer", data_type="FeatureClass", workspace=work)
    arcpy.MultipleRingBuffer_analysis(inputfile, name, distance, "Meters", Outside_Polygons_Only=True)

    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]

    # set symbol and add layer to ArcMap
    res_lyr = arcpy.mapping.Layer(name)
    
    # arcpy.AddMessage(os.path.join(lyr_path, "buffer369.lyr"))
    # if arcpy.Exists(os.path.join(lyr_path, "buffer369.lyr")):
    #     arcpy.AddMessage("okok")
    
    lyr = arcpy.mapping.Layer(os.path.join(lyr_path, "buffer369.lyr"))
    arcpy.mapping.UpdateLayer(df, res_lyr, lyr)
    arcpy.mapping.AddLayer(df, res_lyr)
    arcpy.AddMessage(res_lyr.dataSource)
    arcpy.AddMessage("------------------")

if __name__ == '__main__':
    para1 = arcpy.GetParameterAsText(0)
    make_buffer_ring(para1, 1)