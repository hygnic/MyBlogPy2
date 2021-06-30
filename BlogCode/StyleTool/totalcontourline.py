# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              newcontourline
# Author:            Hygnic
# Created on:        2021/6/1 15:03
# Version:           
# Reference:         
"""
Description:         <<整体轮廓线>>
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
# arcpy.AddMessage("CURRENT: {}".format(os.getcwd()))
# CURRENT: C:\Windows\system32

# 返回工具箱的完整名称
toolbox = os.path.abspath(sys.argv[0])
# arcpy.AddMessage(toolbox)

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




# def merger_all(layer):
#     """
#     一键快速合并一个图层的所有要素(添加一个字段，全部赋值为1，然后融合，最后删除
#     该字段)
#         <特别注意新合成的图层名称，是否会覆盖>
#     layer(String): shp或者lyr文件地址，或者图层对象
#     return: 合并后的新图层 默认返回图层名字为 newlayer_945
#     """
#     arcpy.env.overwriteOutput = True
#     # 判断是否有这个字段
#     global all_fields
#     all_fields = arcpy.ListFields(layer)
#     all_name = [i.name for i in all_fields]
#     name = "test1f2lcc"
#     if name not in all_name:
#         arcpy.AddField_management(layer, name, "LONG")
#     cursor = arcpy.da.UpdateCursor(layer, name)
#     for row in cursor:
#         row[0] = "1"
#         cursor.updateRow(row)
#     del cursor
#     # 完全合并成一个要素
#     dissolve_all = "diss_all_{}".format(randint(0, 10000))
#     arcpy.Dissolve_management(layer, dissolve_all ,name)
#     arcpy.DeleteField_management(dissolve_all, name)
#     arcpy.DeleteField_management(layer, name)
#     return dissolve_all


def better_contour(inputclass, outputclass):
    
    
    arcpy.env.overwriteOutput = True
    arcpy.Merge_management(inputclass, after_merge)



    all_fields = arcpy.ListFields(after_merge)
    all_name = [i.name for i in all_fields]
    name = "test1f2lcc"
    if name not in all_name:
        arcpy.AddField_management(after_merge, name, "LONG")
    cursor = arcpy.da.UpdateCursor(after_merge, name)
    for row in cursor:
        row[0] = "1"
        cursor.updateRow(row)
    del cursor

    arcpy.Dissolve_management(after_merge, "dissolve_all", name)
    arcpy.DeleteField_management("dissolve_all", name)
    arcpy.DeleteField_management(after_merge, name)

    
    after_diss = "dissolve_all"
    arcpy.Delete_management(after_merge)
    print("merge all")
    arcpy.EliminatePolygonPart_management(after_diss,
                                          after_eli,
                                          "AREA",
                                          90000000000,
                                          part_option="CONTAINED_ONLY" )
    arcpy.Delete_management(after_diss)
    print("create contour")
    arcpy.SimplifyPolygon_cartography(after_eli,
                                      outputclass, algorithm="POINT_REMOVE",
                                      tolerance = 1, error_option="NO_CHECK" ,
                                      collapsed_point_option="NO_KEEP")

    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    
    # Update lyr file
    arcpy.AddMessage("-----------")
    lyr = arcpy.mapping.Layer(os.path.join(dir_lyr, "normalline.lyr"))
    outputclass = arcpy.mapping.Layer(outputclass)
    arcpy.mapping.UpdateLayer(df, outputclass, lyr)
    arcpy.AddMessage(outputclass.dataSource)
    arcpy.AddMessage("-----------")
    
    # Add layer to arcmap
    arcpy.mapping.AddLayer(df, outputclass)
    print("complete")
    arcpy.Delete_management(after_eli)

if __name__ == '__main__':
    arcpy.env.overwriteOutput = True

    #-----------name----------------
    # 将所有输入的图层合并
    after_merge = "after_merge_{}".format(randint(0, 10000))
    after_eli = "after_eli_{}".format(randint(0, 10000))

    
    # better_contour([ur"G:\MoveOn\mapping\v103\base.gdb\GBZ"], "new_contour_line")
    output = "output_{}".format(randint(0, 10000))
    shps = arcpy.GetParameterAsText(0).split(";")
    better_contour(shps, output)
    # arcpy.AddMessage(s)
    # arcpy.AddMessage(type(s))