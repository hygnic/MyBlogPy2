#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/1/30 17:04
# Reference:
"""
Description: 自动制图
Usage:
"""
# ---------------------------------------------------------------------------
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import arcpy
import os


"""__________________________________________________________________________"""
"""____________________________global_values_________________________________"""
# 地址
mxd_template = r"E:\doc\Scratch\tempMXDS"  # 模板文件位置
output_dir = r"E:\doc\Scratch\out"  # 输出位置
gdb_path = r"E:\doc\Scratch\arcpy指南.gdb"  # 数据库地址
# 重要常量
FIELD = "CITY" # 检索字段
MI = "MappingIndex" # 制图索引文件名称
SCALE = 200000 # 制图的比例尺

"""____________________________global_values_________________________________"""
"""__________________________________________________________________________"""
arcpy.env.overwriteOutput = True
arcpy.env.workspace = gdb_path


class MakeMXD(object):
    
    def __init__(self,mapdocument, layers_names, mappindex_name, query_fielf, scale=None):
        """
        :param mapdocument: {Object} MXD文件对象
        :param layers_names: {List} 需要设置定义查询语句图层的名称列表
        :param mappindex_name: {String} 索引图层名字；MappingIndex
        :param query_fielf: {String} 定义查询使用的字段名；CITY
        :param scale: {Int} 比例尺
        """
        self.mxd = mapdocument
        self.df = arcpy.mapping.ListDataFrames(self.mxd)[0]
        self.layers = layers_names
        self.index_name = mappindex_name
        self.field = query_fielf
        self.scale = scale
        
        self.mapindex_lyr = arcpy.mapping.ListLayers(self.mxd,self.index_name)[0]
        
        self.mapping_index_query()
        self.make_mxd()
        
        del self.mxd
    
    def mapping_index_query(self):
        """
        给 MappingIndex 图层设置定义查询语句; PAGESIZE = '1080x700'
        :return:
        """
        map_path = self.mxd.filePath
        name = os.path.splitext(os.path.basename(map_path))[0] # 1080x700
        definition_query = ["PAGESIZE"," = ","'",name,"'"]
        self.size = name
        self.mapindex_lyr.definitionQuery = "".join(definition_query)
        # self.mxd.saveACopy(r"E:\doc\Scratch\out\er.mxd")
    
    def make_mxd(self):
        with arcpy.da.SearchCursor(self.mapindex_lyr, self.field) as cursor:
            for row in cursor: # 提前解包？
                name = row[0]
                self.define_query(name) # 定义查询
                self.center_scale(name) # 居中
                self.change_txt(name) # 修改文本
                self.label_query(name) # 标注查询语句
                arcpy.SelectLayerByAttribute_management(self.mapindex_lyr, "CLEAR_SELECTION") # 取消该图层的所有选择选择项目
                self.saveacopy(name) # 另存
    
    def define_query(self, value):
        """
        定义查询
        :param value: {String/Int/Float} 用于定义查询的值
        :return: None
        """
        for layer in self.layers:
            lyr = arcpy.mapping.ListLayers(self.mxd, layer)[0]
            d_q = ['"',self.field,'"'," = ","'",value,"'"]
            # lyr.definitionQuery = '"' + FIELD + '"' + " = " + "'" + value + "'"
            lyr.definitionQuery = "".join(d_q)
    
    def center_scale(self, name):
        """
        使图框居中并设置比例尺
        :param name: {String/Int/Float} 用于查询语句的值
        :return: None
        """
        where_clause = "{} = '{}'".format(self.field, name)
        arcpy_slba = arcpy.SelectLayerByAttribute_management
        arcpy_slba(self.mapindex_lyr, "NEW_SELECTION", where_clause)
        self.df.extent = self.mapindex_lyr.getSelectedExtent()
        if self.scale:
            self.df.scale = self.scale
    
    def change_txt(self, name):
        # 修改文本
        for elm in arcpy.mapping.ListLayoutElements(self.mxd, 'TEXT_ELEMENT'):
            if elm.text == "XX市铁路交通分布演示草图":
                elm.text = "XX市铁路交通分布演示草图".replace("XX市", name)
    
    def label_query(self,name):
        # 设置标注的查询语句
        lyr_label = arcpy.mapping.ListLayers(self.mxd, "市级区域")[0]
        if lyr_label.supports("LABELCLASSES"):
            query = ["NOT","( ", self.field, "=", "'", name, "'", " )"] # NOT( CITY = '巴中市' )
            for lblClass in lyr_label.labelClasses:
                lblClass.SQLQuery = "".join(query)
    
    def saveacopy(self, name):
        # 另存
        self.mxd.saveACopy(output_dir+'/'+name+'.mxd')
        print("Complete <name: {} size: {}> ".format(name, self.size))


# 运行窗口
if __name__ == '__main__':
    for a_mxd in [x for x in os.listdir(mxd_template) if ".mxd" or ".MXD" in x]:
        mxd_fullpath = os.path.join(mxd_template, a_mxd)
        mxd = arcpy.mapping.MapDocument(mxd_fullpath)
        MakeMXD(mxd, ["roads","railways","landuse","natural","buildings"], MI, FIELD, SCALE)