# -*- coding:cp936 -*-
# -------------------------------------------
# ʹ�� cp936 ������Խ�����ĵ��빤�������������
# arcpy.AddMessage("\n|---------------------------------|")
# arcpy.AddMessage(" -----  ������ GIS�� ����������  ------")
# arcpy.AddMessage("|---------------------------------|\n")

# Name:              SolidBoundaryLine
# Author:            Hygnic
# Created on:        2022/7/6 21:55
# Version:           
# Reference:
"""
Description:         ����߽�Ч��>>��ͼ��ת��Ϊ��ͼ�㡢��ͼ���Ч����ƫ������
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys
from random import randint


def merger_all(layer, outputclass= "in_memory/diss_all"):
    """
    һ�����ٺϲ�һ��ͼ�������Ҫ��(���һ���ֶΣ�ȫ����ֵΪ1��Ȼ���ںϣ����ɾ��
    ���ֶ�)
        <�ر�ע���ºϳɵ�ͼ�����ƣ��Ƿ�Ḳ��>
    layer(String): shp����lyr�ļ���ַ������ͼ�����
    return: �ϲ������ͼ�� Ĭ�Ϸ���ͼ������Ϊ newlayer_945
    """
    arcpy.env.addOutputsToMap = False
    arcpy.env.overwriteOutput = True
    # �ж��Ƿ�������ֶ�
    
    all_fields = arcpy.ListFields(layer)
    all_name = [i.name for i in all_fields]
    # for f in all_fields:
    # 	print f.name #Todo  neme �� aliasName ���صĶ�һ����Ϊʲô
    # print f.aliasName
    
    name = "test1f2lcc"
    if name not in all_name:
        arcpy.AddField_management(layer, name, "LONG")
    cursor = arcpy.da.UpdateCursor(layer, name)
    for row in cursor:
        row[0] = "1"
        cursor.updateRow(row)
    del cursor
    # new_ly = "newlayer_945"
    # ʹ���ڴ�ռ�
    
    new_ly = outputclass
    arcpy.Dissolve_management(layer, new_ly ,name)
    arcpy.DeleteField_management(new_ly, name)
    return outputclass


def update_representation(inputfile, rep_lyr, output_re, border):
    """
    ��ͼ�����ָ������ͼ���Ч������ӵ� ArcMap ��
    :param inputfile: ����ͼ��
    :param rep_lyr: {String} ��ͼ���ͼ�����ƣ�.lyr file��
    :param output_re: ���ͼ��
    :param border: ����ֵ �Ƿ��������������
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
    # in_lyr = arcpy.mapping.Layer(inputfile)
    if border == "true":
        in_lyr = merger_all(inputfile)
    else:
        in_lyr = inputfile
    
    randnum = randint(0, 999999)
    lyr_randname = "%scratchGDB%/lyr_{}".format(randnum)
    arcpy.FeatureToLine_management(in_lyr, lyr_randname)
    
    ####### Create a new layer
    arcpy.CopyFeatures_management(lyr_randname, output_re)
    new_lyr = arcpy.mapping.Layer(os.path.join(work, output_re))
    
    ####### Make representation symbol to new layer
    representation_lyr = arcpy.mapping.Layer(rep_lyr)
    arcpy.AddMessage("------------------")
    # representation name
    randnum = randint(0, 999999)
    rp_name = "Rep_{}".format(randnum)
    
    ####### Create Representation
    r_func = arcpy.AddRepresentation_cartography
    r_func(new_lyr, rp_name, import_rule_layer=representation_lyr) #####
    ###### copy transparency value
    opacity = representation_lyr.transparency
    new_lyr.transparency = opacity
    
    #       add new layer to arcmap
    arcpy.SetLayerRepresentation_cartography(new_lyr, rp_name)
    arcpy.mapping.AddLayer(df, new_lyr)
    arcpy.Delete_management(lyr_randname)
    arcpy.Delete_management(in_lyr)
    arcpy.AddMessage(new_lyr.dataSource)
    arcpy.AddMessage("------------------")


def add_background_layer(path_toolbox, input_fc, output, transparency):
    """
    ��ӱ���ͼ��
    :param path_toolbox: ����·�����ɻ��lyr�����ݿ�·��
    :param input_fc: ����Ҫ�أ�Ȼ�����
    :param output: ���·�������汳��ͼ��Ĵ��λ��
    :param transparency: ͸��������
    :return:
    """
    ##### Add backgroud layer and erase
    retangle_world = os.path.join(path_toolbox,
                                  "Representation",
                                  "rep_base.gdb",
                                  "FeatureClass_RetangleWorld3857")
    retangle_world = arcpy.mapping.Layer(retangle_world)
    # Output background
    bg_lyr_name = arcpy.CreateScratchName(prefix="BgP", workspace=os.path.join(os.path.dirname(output)))
    arcpy.Erase_analysis(retangle_world, input_fc, bg_lyr_name)
    # bg_lyr_name_proj = arcpy.CreateScratchName(prefix="Bg", workspace=os.path.join(os.path.dirname(output)))
    # arcpy.Project_management(bg_lyr_name, bg_lyr_name_proj, input_fc)
    bg_lyr = arcpy.mapping.Layer(bg_lyr_name)
    
    ##### Update lyr file and add layer to mxd
    path_lyr_dir = os.path.join(path_toolbox, "lyr")
    # Get .lyr file and convert to Layer object
    lyr_style = os.path.join(path_lyr_dir, "Background1.lyr")
    lyr_style = arcpy.mapping.Layer(lyr_style)
    # Get MXD and Dataframe object
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = mxd.activeDataFrame
    # Update and add
    arcpy.mapping.UpdateLayer(df, bg_lyr, lyr_style)
    bg_lyr.transparency = int(transparency)
    arcpy.mapping.AddLayer(df, bg_lyr)
    del mxd
    del df

if __name__ == '__main__':
    #------------------------------
    #------------path--------------
    # ���ع��������������
    
    toolbox = os.path.abspath(sys.argv[0])
    arcpy.AddMessage(toolbox)
    # E:\Document\MoveOn\MyBlogPy2\BlogCode\StyleToolCode\SolidBoundaryLine.py

    #@@ δ���빤������
    
    # tool_dir = os.path.abspath(os.path.join(os.path.dirname(toolbox),"StyleTool"))
    #@@ Run in toolbox
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # lyr
    dir_lyr = os.path.join(tool_dir, "lyr") # StyleTool/lyr
    # ��ͼ������
    
    representation = os.path.join(tool_dir, "Representation")
    rp_gdb = os.path.join(representation, "rep_base.gdb")
    #------------path--------------
    #------------------------------
    
    #------------------------------
    #----------workspace-----------
    arcpy.env.workspace = os.path.dirname(arcpy.GetParameterAsText(1))
    work = arcpy.env.workspace
    
    add_background_layer(tool_dir,
                         arcpy.GetParameterAsText(0),
                         arcpy.GetParameterAsText(1),
                         arcpy.GetParameterAsText(2))
    
    
    rep_lyrr = os.path.join(representation, "SolidBoundaryLine.lyr")
    update_representation(arcpy.GetParameterAsText(0), rep_lyrr,
                          arcpy.GetParameterAsText(1),
                          arcpy.GetParameterAsText(3))
    
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  ������ GIS�� ����������  ------")
    arcpy.AddMessage("|---------------------------------|\n")