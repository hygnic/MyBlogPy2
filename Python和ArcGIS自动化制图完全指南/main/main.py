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
from os.path import splitext as st
from os import listdir as ld




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


def size_creator(path):
    """
    根据输入的模板文件地址生成标准格式的字典。
    :param path: {String} mxd file path
    :return: {Dict} such as: {'pagesize3': (1180, 900), 'pagesize2': (1080, 700), 'pagesize1': (1080, 1300)}
    """
    print("请确保模板文件夹中不存在无关文件！")
    m_dict = {}
    counter = 1
    for m_name in [st(x)[0] for x in ld(path) if ".mxd" or ".MXD" in x]:
        width, height = m_name.split("x")
        name = "pagesize{}".format(counter)
        m_dict[name] = (int(width), int(height))
        counter += 1
    # {
    #     "pagesize1":(1080,700),
    #     "pagesize2":(1080,1300),
    #     "pagesize3":(1180,900)
    # }
    return m_dict


def select_template_size(size, template_size):
    """
    根据给出的size大小去 template_size字典中匹配大小合适的模板，然后返回名称，如 pagesize3
    :param size:  宽和高组成的列表
        such as:[659.8490915000066, 822.3146429999917]
    :param template_size: 制图模板大小
    :return: 返回制图模板大小的名称（键），
        如果找不到适合的制图模板就返回 -1
    """
    map_w, map_h = size[0], size[1]
    map_div = map_w / map_h
    # 符合该制图单位的模板大小的字典
        # 字典推导式，生成如这样的字典：{... , "达州市" : (宽，高，面积大小，宽高比例)  , ...}。
        # ... v[0]>map_w and v[1]>map_h...  这段代码做了初步的筛选，筛选出满足该制图单位宽和高的 mxd模板。
        # 同时这里引入了 面积 和 宽高比例，这两个指标用于进一步的判断和筛选。
    template_size_fit = {
        k:(v[0], v[1], v[0]*v[1], v[0]/v[1]) for k,v
        in template_size.items() if v[0]>map_w and v[1]>map_h
    }
    d_len = len(template_size_fit)
    # 字典转列表
    d2l = zip(template_size_fit.keys(), template_size_fit.values())
    # 按元组中第三个数大小排序（按面积大小）
    d2l_sorted = sorted(d2l, key=lambda x: x[1][2])
    if d_len > 2:
        two_remaind = d2l_sorted[:2]
        # (u'pagesize3', (1380, 850, 1173000, 1.6235294117647059))
        res = min(two_remaind, key=lambda x: abs(x[1][3]-map_div))
        return res[0] # u'pagesize3'
    elif d_len==2:
        res = d2l_sorted[0]
        return res[0]
    elif d_len==1:
        return d2l_sorted[0][0]
    else:
        # info="存在超出页面大小的制图单位"
        return -1


def check_field(layer, field):
    """
    检查一个要素文件中是否存在field字段
    """
    fields = arcpy.ListFields(layer)
    return field in [_.name for _ in fields]



class PageSizeMatch(object):
    """
    适配页面大小
    """
    def __init__(self, feature_name, field, mxd_template_d):
        """
        :param feature_name: {String} # 制图索引图层的名字
        :param field: {String} field = "CITY" # 检索字段
        :param mxd_template_d: {Dict} 模板匹配信息（字典）
        """
        self.f = feature_name # 制图索引图层的名字
        self.field = field
        self.m_d = mxd_template_d
        self.minimum_bounding() # 制作最小几何边界图层
        true_height = self.check_width_height() # 获取真实的高度信息
        # 将高度信息更新入制图索引图层（MappingIndex）
        self.update_width_height(true_height)
        self.update_page_size(SCALE)
    
    def minimum_bounding(self):
        """
        1.make MinimumBoundingGeometry feature layer
        2.add PAGRSIZE field
        :return:
        """
        if not check_field(MI,"MBG_Width"):
            mbe = arcpy.MinimumBoundingGeometry_management
            mbe(self.f, "m_out", "ENVELOPE", "LIST", self.field, True)
            print("Complete MinimumBoundingGeometry")
            arcpy.Delete_management(self.f,"FeatureClass")
            arcpy.Rename_management("m_out",self.f,"FeatureClass")
        
        if not check_field(self.f,"PAGESIZE"):
            # 没有计算过最小几何边界
            print('Add field PAGESIZE')
            arcpy.AddField_management(
                self.f, "PAGESIZE", "TEXT", field_length = 100)
    
    def check_width_height(self):
        # 使用 “要素折点转点要素” 工具，将最小边界几何转变成点；
        # 每一个最小边界几何都会生成5个点：左下，左上，右上，右下，左下；
        # 前两个点的差值就是高度
        # 返回值为高度的字典：{地级市名称：高度}
        # {..."广安市":879.2, "巴中市":124.56, "桂林市":54.7801, ...}
        fea_v = "feature_vertices" # feature name
        short_f = arcpy.FeatureVerticesToPoints_management
        short_f(self.f, fea_v, "ALL")
        cursor = arcpy.da.SearchCursor(fea_v, [self.field, "SHAPE@Y"])
        cursor2l = [(x[0],x[1]) for x in cursor] # 转换成列表
        del cursor
        # [(u'\u5df4\u4e2d\u5e02', 3460475.693600001),
        # (u'\u5df4\u4e2d\u5e02', 3331847.4146)]
        # 每个矩形都会生成5个按顺序排列的点，cursor2l[::5] 使用切片每隔5个数取第一个；cursor2l[1::5] 使用切片每隔5个数取第二个。
        cursor2l_1 , cursor2l_2 = cursor2l[::5], cursor2l[1::5]
        height_info = {}
        # 这个 for 循环是将 y 轴差值和制图单位名称组合成字典。
        for i in xrange(len(cursor2l_1)):
            height = cursor2l_2[i][1] - cursor2l_1[i][1]
            height_info[cursor2l_2[i][0]] = abs(height)
        return height_info
    

    def update_width_height(self, height_infomation):
        """
        height_infomation 形参接收上面 check_width_height 方法的返回值。
        该方法会把 MappingIndex 图层中的 "MBG_Width","MBG_Length"两字段更新为宽和高
        :param height_infomation: {Dict} 包含了制图单位的高度信息
        :return:
        """
        _field = [self.field,"MBG_Width", "MBG_Length"]
        with arcpy.da.UpdateCursor(self.f, _field) as cursor:
            for row in cursor:
                name, width, height = row
                # 如果短边等于高度，字段 MBG_Width 和 MBG_Length 的意义从原来的短边和长边变成宽和高，
                # 那么原来 MBG_Width 和 MBG_Length 的值就需要互换。
                if round(height_infomation[name], 2) == round(width, 2):
                    row[1] = height
                    row[2] = width
                cursor.updateRow(row)
        print("updating width&height……")
    
    
    def update_page_size(self,scale):
        """
        更新填充字段 "PAGESIZE" 的值
        :param scale: {Int} 比例大小
        :return:
        """
        _field = ["MBG_Width", "MBG_Length", "PAGESIZE"]
        with arcpy.da.UpdateCursor(self.f, _field) as cursor:
            for row in cursor:
                row_p = [row[0], row[1]]
                #单位换算成了毫米 [659.8490915000066, 822.3146429999917]
                new_row = [x/scale*1000 for x in row_p]
                # PAGESIZE1 or -1
                pgs_name = select_template_size(new_row, self.m_d)
                if pgs_name != -1:
                    p_size = self.m_d[pgs_name] # (1180, 900)
                    # update PAGESIZE field values 1180x900
                    row[2] = "{}x{}".format(p_size[0],p_size[1])
                else:
                    print("存在超出所有模板页面大小的制图单位")
                cursor.updateRow(row)
        print("update PAGESIZE completly!")



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
        self.idx = idx
        self.field = query_fielt
        self.scale = scale
        
        # MappingIndex
        self.mapidx = arcpy.mapping.ListLayers(self.mxd,self.idx)[0]
        
        self.mapping_index_query()
        self.make_mxd()
        
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
       
        with arcpy.da.SearchCursor(self.mapidx, self.field) as cursor:
            for row in cursor:
                name = row[0]
                self.define_query(name) # 定义查询
                self.center_scale(name) # 居中
                self.change_txt(name) # 修改文本
                self.label_query(name) # 标注查询语句
                # 取消该图层的所有选择选择项目
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
        sba(self.mapidx, "NEW_SELECTION", where_clause)
        self.df.extent = self.mapidx.getSelectedExtent()
        if self.scale:
            self.df.scale = self.scale
    
    def change_txt(self, name):
        # 修改文本
        map_title = "XX市铁路交通分布演示草图"
        for elm in arcpy.mapping.ListLayoutElements(
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
        self.mxd.saveACopy(output_dir+'/'+name+'.mxd', "10.1")
        print("Complete <name: {} size: {}> ".format(name, self.size))
        



if __name__ == '__main__':
    
    # 第三章 分配模板，更新 PAGESIZE 字段
    mxd_d = size_creator(mxd_template)
    PageSizeMatch(MI, FIELD, mxd_d)
    
    # 第四章 自动制图
    for a_mxd in [x for x in os.listdir(mxd_template)
                  if ".mxd" or ".MXD" in x]:
        
        mxd_fullpath = os.path.join(mxd_template, a_mxd)
        mxd = arcpy.mapping.MapDocument(mxd_fullpath)
        
        MakeMXD(
            mxd,
            ["roads","railways","landuse","natural","buildings"],
            MI, FIELD, SCALE
        )