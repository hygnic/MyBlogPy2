# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              LumiContour
# Author:            Hygnic
# Created on:        2021/5/31 12:46
# Version:           
# Reference:         
"""
Description:         �������� 9�����壬ͬһ����ɫ������͸����
                     ���ν���
                     ʹ�� opacity.lyr
                     �Ѿ����빤���� <<��������>>
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys
from random import randint



class OpacityContour(object):
    # ����͸����������Ե��
    # 1.�ȴ���9�㻺����
    # 2.�½��ֶ����ڴ�Ų�ͬ���𻺳�����͸����
    
    def __init__(self, in_f, times, lyr, output):
        """
        :param in_f: ����Ҫ��
        :param times: �Ŵ���
        :param lyr: lyr Ч��ͼ��
        :param output: ��ʽͼ�����
        """
        self.mxd = arcpy.mapping.MapDocument("CURRENT")
        self.df = arcpy.mapping.ListDataFrames(self.mxd)[0]
        
        self.in_f = in_f
        self.times = times
        self.lyr = arcpy.mapping.Layer(lyr)
        self.output = output
        
        self.distance = [i*10 for i in xrange(1, 10)]
        
        self.make_buffer_ring()
        self.set_opacity()
        arcpy.Delete_management(self.buffered)

    def make_buffer_ring(self):
        arcpy.AddMessage("Making buffer rings����")
        num = int(self.times)
        inputfile = self.in_f
        distance = [_*num for _ in self.distance]
        # self.buffered = arcpy.CreateScratchName(prefix="buffered", workspace=os.path.join(os.path.dirname(self.output)))
        buffername = "in_memory/ne"+str(randint(1, 10000))
        self.buffered = buffername
        arcpy.MultipleRingBuffer_analysis(inputfile, self.buffered, distance, "Meters", Outside_Polygons_Only=True)
        
        # ����ͬ����Ļ������ϲ�����Ϊ��ĳЩ����£�ͬһ����Ļ��������ܻ��ɼ���Ҫ��
        # Dissolve same distance feature
        arcpy.Dissolve_management(self.buffered, self.output, dissolve_field="distance", statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
        # set symbol and add layer to ArcMap
        self.res_lyr = arcpy.mapping.Layer(self.output)
        # self.res_lyr = arcpy.mapping.Layer(inputfile)
        
        
    def set_opacity(self):
        f_name = "opacity"
        arcpy.AddMessage("Apply style setting����")
        # self.add_field(self.res_lyr, [f_name], "SHORT")

        arcpy.AddField_management(self.res_lyr, f_name, "SHORT", field_length="")
        
        with arcpy.da.UpdateCursor(self.res_lyr, f_name) as cursor:
            in_count = 0
            for row in cursor:
                row[0] = self.distance[in_count]
                in_count += 1
                cursor.updateRow(row)
        arcpy.mapping.UpdateLayer(self.df,  self.res_lyr, self.lyr)
        arcpy.mapping.AddLayer(self.df, self.res_lyr)
        arcpy.AddMessage(self.res_lyr.dataSource)

    
if __name__ == '__main__':
    #------------------------------
    #------------path--------------
    #       �ڵ���������
    # arcpy.AddMessage("CURRENT: {}".format(os.getcwd()))
    # CURRENT: C:\Windows\system32

    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  ������ GIS�� ����������  ------")
    arcpy.AddMessage("|---------------------------------|\n")


# ���ع��������������
    toolbox = os.path.abspath(sys.argv[0])
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # lyr
    dir_lyr = os.path.join(tool_dir, "lyr") # StyleTool/lyr
    # ��ͼ����ļ��洢λ��
    representation = os.path.join(tool_dir, "Representation")
    rp_gdb = os.path.join(representation, "rep_base.gdb")
    #------------path--------------
    #------------------------------
    
    #------------------------------
    #----------workspace-----------
    arcpy.env.workspace = os.path.dirname(arcpy.GetParameterAsText(2))
    work = arcpy.env.workspace
    #----------workspace-----------
    #------------------------------



    # arcpy.env.addOutputsToMap = True
    lyr_file = os.path.join(dir_lyr, "opacity.lyr")
    OpacityContour(arcpy.GetParameterAsText(0),
                   arcpy.GetParameterAsText(1), lyr_file,
                   arcpy.GetParameterAsText(2))