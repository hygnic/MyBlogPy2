# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              OpacityContour
# Author:            Hygnic
# Created on:        2021/5/31 12:46
# Version:           
# Reference:         
"""
Description:         <<����������>> ����ѡ�񻺳���������
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys



class BufferContour(object):
    # �������������Ե��
    # 1.�ȴ���3�㻺����
    # 2.�½��ֶ����ڴ�Ų�ͬ����Ļ�����
    
    def __init__(self, in_f, times, lyr, output):
        self.mxd = arcpy.mapping.MapDocument("CURRENT")
        self.df = arcpy.mapping.ListDataFrames(self.mxd)[0]
        
        self.in_f = in_f
        self.times = times
        self.output = output
        self.lyr = arcpy.mapping.Layer(lyr)
        
        self.distance = [1, 2, 3]
        
        self.make_buffer_ring()
        self.set_symbol()

    def make_buffer_ring(self):
        num = int(self.times)
        inputfile = self.in_f
        distance = [_*30*num for _ in self.distance]
        arcpy.MultipleRingBuffer_analysis(inputfile, self.output, distance, "Meters", Outside_Polygons_Only=True)
        
        # set symbol and add layer to ArcMap
        self.res_lyr = arcpy.mapping.Layer(self.output)
        # self.res_lyr = arcpy.mapping.Layer(inputfile)
        
        
    def set_symbol(self):
        f_name = "buffer01"
        arcpy.AddMessage("Set Symbols")
        self.add_field(self.res_lyr, [f_name], "SHORT")

        with arcpy.da.UpdateCursor(self.res_lyr, f_name) as cursor:
            in_count = 0
            for row in cursor:
                row[0] = self.distance[in_count]
                in_count += 1
                cursor.updateRow(row)
        arcpy.mapping.UpdateLayer(self.df,  self.res_lyr, self.lyr)
        arcpy.mapping.AddLayer(self.df, self.res_lyr)
        arcpy.AddMessage(self.res_lyr.dataSource)
        arcpy.AddMessage("------------------\n")
        
    """--------------------------------"""
    """--------------------------------"""
    """Add Field"""
    def check_field_exit(self, field_obj, check_field):
        """
        ���ͼ���Ƿ���ڸ��ֶ�
        :param field_obj: field_obj = arcpy.ListFields(layer)
        :param check_field: field
        :return: {Bolean}
        """
        field_names = [i.name for i in field_obj] # field.aliasName
        return check_field in field_names
    
    
    def add_field(self, layer, names, f_type, f_length=None, delete=True):
        """�����ͬ���ͺͳ��ȵĶ�����ߵ����ֶΣ�ֻ֧��Ҫ��ͼ��(���������ͬ���ֵ��ֶ��򲻻�����ֶ�)
          <�ر�ע����Ϊ�ֶ����ͺͳ�����ɵĺ�������>
          such as: add_field(layer_p,["ZWMC1","ZWMC2"],"TEXT",50)
        layer{String}: shp�ļ�����
          # TODO ����Ӧ�ÿ���ʹ��ͼ�����arcpy.mapping.Layer(path)�����Ǳ���arcgis10.3��
              # �Ѿ������ ��Ϊarcpy.AddField_management ֻ֧��Ҫ��ͼ�㣬�����shp�ļ���ַ�Ļ�
              # ��Ҫʹ��arcpy.MakeFeatureLayer_management������Ҫ����תΪҪ��ͼ��
        names: {List} �����ֶ�����
        f_type: {String} �ֶ�����
        f_length: {Long} �ֶγ���
        delete: {Boolean} True ������ڸ��ֶΣ���ɾ���ٴ���
        return: ���ص�ǰ��ͼ�����
        """
        the_fields = arcpy.ListFields(layer)
        for name in names:
            if not self.check_field_exit(the_fields, name):
                arcpy.AddField_management(layer, name, f_type, field_length=f_length)
                msg = "Created {0} field success".format(name)
                print msg
            # ���ڸ��ֶ�
            else:
                if delete:
                    arcpy.DeleteField_management (layer, name)
                    arcpy.AddField_management(layer, name, f_type, field_length=f_length)
                else:
                    print "Field exist"
        
        return layer
    """Add Field"""
    """--------------------------------"""
    """--------------------------------"""
    

if __name__ == '__main__':
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  ������ GIS�� ����������  ------")
    arcpy.AddMessage("|---------------------------------|\n")
    
    #------------------------------
    #------------path--------------
    #       �ڵ���������
    # arcpy.AddMessage("CURRENT: {}".format(os.getcwd()))
    # CURRENT: C:\Windows\system32
    
    # ���ع��������������
    toolbox = os.path.abspath(sys.argv[0])
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # get style lyr path
    dir_lyr = os.path.join(tool_dir, "lyr") # StyleTool/lyr
    #------------path--------------
    #------------------------------
    
    #------------------------------
    #----------workspace-----------
    arcpy.env.workspace = os.path.dirname(arcpy.GetParameterAsText(2))
    work = arcpy.env.workspace
    #----------workspace-----------
    #------------------------------
    
    # arcpy.env.addOutputsToMap = True
    lyr_file = os.path.join(dir_lyr, "buffer369.lyr")
    BufferContour(arcpy.GetParameterAsText(0),
                     arcpy.GetParameterAsText(1), lyr_file,
                  arcpy.GetParameterAsText(2))