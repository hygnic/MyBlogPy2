# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              newcontourline
# Author:            Hygnic
# Created on:        2021/6/1 15:03
# Version:           
# Reference:         
"""
Description:         <<��������>>
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys
from random import randint


# def merger_all(layer):
#     """
#     һ�����ٺϲ�һ��ͼ�������Ҫ��(���һ���ֶΣ�ȫ����ֵΪ1��Ȼ���ںϣ����ɾ��
#     ���ֶ�)
#         <�ر�ע���ºϳɵ�ͼ�����ƣ��Ƿ�Ḳ��>
#     layer(String): shp����lyr�ļ���ַ������ͼ�����
#     return: �ϲ������ͼ�� Ĭ�Ϸ���ͼ������Ϊ newlayer_945
#     """
#     arcpy.env.overwriteOutput = True
#     # �ж��Ƿ�������ֶ�
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
#     # ��ȫ�ϲ���һ��Ҫ��
#     dissolve_all = "diss_all_{}".format(randint(0, 10000))
#     arcpy.Dissolve_management(layer, dissolve_all ,name)
#     arcpy.DeleteField_management(dissolve_all, name)
#     arcpy.DeleteField_management(layer, name)
#     return dissolve_all


def whole_contour(inputclass, outputclass):
    
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
    #------------------------------
    #------------path--------------
    #       �ڵ���������
    # arcpy.AddMessage("CURRENT: {}".format(os.getcwd()))
    # CURRENT: C:\Windows\system32
    
    # ���ع��������������
    toolbox = os.path.abspath(sys.argv[0])
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # lyr
    dir_lyr = os.path.join(tool_dir, "lyr") # StyleTool/lyr
    #------------path--------------
    #------------------------------
    
    #------------------------------
    #----------workspace-----------
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = os.path.dirname(arcpy.GetParameterAsText(1))
    work = arcpy.env.workspace
    #----------workspace-----------
    #------------------------------
    
    

    #-----------name----------------
    # �����������ͼ��ϲ�
    after_merge = "after_merge_{}".format(randint(0, 10000))
    after_eli = "after_eli_{}".format(randint(0, 10000))

    
    # better_contour([ur"G:\MoveOn\mapping\v103\base.gdb\GBZ"], "new_contour_line")
    shps = arcpy.GetParameterAsText(0).split(";")
    whole_contour(shps, arcpy.GetParameterAsText(1))
    # arcpy.AddMessage(s)
    # arcpy.AddMessage(type(s))