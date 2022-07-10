# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              OpacityContour
# Author:            Hygnic
# Created on:        2021/5/31 12:46
# Version:           
# Reference:         
"""
Description:         <<缓冲区轮廓>> 可以选择缓冲区扩大倍数
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys



class BufferContour(object):
    # 创建缓冲区外边缘。
    # 1.先创建3层缓冲区
    # 2.新建字段用于存放不同级别的缓冲区
    
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
    """字段添加"""
    def check_field_exit(self, field_obj, check_field):
        """
        检查图层是否存在该字段
        :param field_obj: field_obj = arcpy.ListFields(layer)
        :param check_field: field
        :return: {Bolean}
        """
        field_names = [i.name for i in field_obj] # field.aliasName
        return check_field in field_names
    
    
    def add_field(self, layer, names, f_type, f_length=None, delete=True):
        """添加相同类型和长度的多个或者单个字段，只支持要素图层(如果存在相同名字的字段则不会添加字段)
          <特别注意因为字段类型和长度造成的后续错误>
          such as: add_field(layer_p,["ZWMC1","ZWMC2"],"TEXT",50)
        layer{String}: shp文件对象
          # TODO 按理应该可以使用图层对象，arcpy.mapping.Layer(path)，但是报错（arcgis10.3）
              # 已经解决： 因为arcpy.AddField_management 只支持要素图层，如果是shp文件地址的话
              # 需要使用arcpy.MakeFeatureLayer_management函数将要素类转为要素图层
        names: {List} 新增字段名称
        f_type: {String} 字段类型
        f_length: {Long} 字段长度
        delete: {Boolean} True 如果存在该字段，先删除再创建
        return: 返回当前的图层对象
        """
        the_fields = arcpy.ListFields(layer)
        for name in names:
            if not self.check_field_exit(the_fields, name):
                arcpy.AddField_management(layer, name, f_type, field_length=f_length)
                msg = "Created {0} field success".format(name)
                print msg
            # 存在该字段
            else:
                if delete:
                    arcpy.DeleteField_management (layer, name)
                    arcpy.AddField_management(layer, name, f_type, field_length=f_length)
                else:
                    print "Field exist"
        
        return layer
    """字段添加"""
    """--------------------------------"""
    """--------------------------------"""
    

if __name__ == '__main__':
    arcpy.AddMessage("------------------")
    #------------------------------
    #------------path--------------
    #       在导入的情况下
    # arcpy.AddMessage("CURRENT: {}".format(os.getcwd()))
    # CURRENT: C:\Windows\system32
    
    # 返回工具箱的完整名称
    toolbox = os.path.abspath(sys.argv[0])
    
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # lyr
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