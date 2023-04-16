# -*- coding:utf-8 -*-
# ----------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/1/29 17:34
# ----------------------------------------------------------
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import arcpy
import os


"""_______global_values_______"""
# 地址
mxd_template = "E:/doc/main/tempMXDS"  # 模板文件位置
output_dir = "E:/doc/main/out"  # 制图输出位置
gdb_path = "E:/doc/main/arcpy指南.gdb"  # 数据库地址
# 重要常量
FIELD = "CITY" # 检索字段
MI = "MappingIndex" # 制图索引文件名称
SCALE = 200000 # 制图的比例尺
"""_______global_values_______"""

arcpy.env.overwriteOutput = True
arcpy.env.workspace = gdb_path

sba = arcpy.SelectLayerByAttribute_management


class MakeMXD(object):
    
    def __init__(self, m, lyrs, idx, query_fielt, scale=None):
        """
        :param m: {Object} MXD文件对象
        :param lyrs: {List} 需要设置定义查询语句图层的名称列表
        :param idx: {String} 索引图层名字；MappingIndex
        :param query_fielt: {String} 定义查询使用的字段名；CITY
        :param scale: {Int} 比例尺
        """
        self.mxd = m
        self.df = arcpy.mapping.ListDataFrames(self.mxd)[0]
        self.lyrs = lyrs
        self.idx_name = idx
        self.field = query_fielt
        self.scale = scale
        
        # MappingIndex
        self.mapidx = arcpy.mapping.ListLayers(self.mxd,self.idx)[0]
        
        self.mapping_index_query()
        self.make_mxd() # ▶注释1◀
        
        del self.mxd
    
    def mapping_index_query(self):
        """
        给 MappingIndex 图层设置定义查询语句;
            PAGESIZE = '1080x700'
        :return:
        """
        map_path = self.mxd.filePath
        name = os.path.splitext(os.path.basename(map_path))[0]
        definition_query = ["PAGESIZE"," = ","'",name,"'"]
        self.size = name
        self.mapidx.definitionQuery = "".join(definition_query)
    
    def make_mxd(self):
        # ▶注释2◀
        with arcpy.da.SearchCursor(self.mapidx, self.field) as cursor:
            for row in cursor: # 提前解包？
                name = row[0]
                self.define_query(name) # 定义查询
                self.center_scale(name) # 居中
                self.change_txt(name) # 修改文本
                self.label_query(name) # 标注查询语句
                # 取消该图层的所有选择选择项目 ▶注释3◀
                sba(self.mapidx, "CLEAR_SELECTION")
                self.saveacopy(name) # 另存
    
    def define_query(self, value):
        """
        定义查询
        :param value: {String/Int/Float} 用于定义查询的值
        :return: None
        """
        for layer in self.lyrs:
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
        sba(self.mapidx, "NEW_SELECTION", where_clause) # ▶注释1◀
        self.df.extent = self.mapidx.getSelectedExtent()
        if self.scale:
            self.df.scale = self.scale
    
    def change_txt(self, name):
        # 修改文本
        map_title = "XX市铁路交通分布演示草图"
        for elm in arcpy.mappng.ListLayoutElements(
                self.mxd, 'TEXT_ELEMENT'):
            if elm.text == map_title:
                elm.text = map_title.replace("XX市", name)
    
    def label_query(self,name):
        # 设置标注的查询语句
        lyr_label = arcpy.mapping.ListLayers(self.mxd, "市级区域")[0]
        if lyr_label.supports("LABELCLASSES"):
            # NOT( CITY = '巴中市' )
            query = ["NOT","( ", self.field, "=", "'", name, "'", " )"]
            for lblClass in lyr_label.labelClasses:
                lblClass.SQLQuery = "".join(query)
    
    def saveacopy(self, name):
        # 另存
        self.mxd.saveACopy(output_dir+'/'+name+'.mxd')
        print("Complete <name: {} size: {}> ".format(name, self.size))


# 运行窗口
if __name__ == '__main__':
    for a_mxd in [x for x in os.listdir(mxd_template)
                  if ".mxd" or ".MXD" in x]:
        mxd_fullpath = os.path.join(mxd_template, a_mxd)
        mxd = arcpy.mapping.MapDocument(mxd_fullpath)
        MakeMXD(
            mxd,
            ["roads","railways","landuse","natural","buildings"],
            MI, FIELD, SCALE
        ) # ▶注释4◀