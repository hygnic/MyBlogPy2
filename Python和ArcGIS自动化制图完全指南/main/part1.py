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
    template_size_fit = {
        k:(v[0], v[1], v[0]*v[1], v[0]/v[1]) for k,v
        in template_size.items() if v[0]>map_w and v[1]>map_h
    } #▶注释6◀
    d_len = len(template_size_fit)
    # 字典转列表
    d2l = zip(template_size_fit.keys(), template_size_fit.values())
    # 按元组中第三个数大小排序（按面积大小）
    d2l_sorted = sorted(d2l, key=lambda x: x[1][2])
    if d_len > 2: #▶注释7◀
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
        if not check_field(MI,"MBG_Width"): #▶注释1◀
            #▶注释2◀
            mbe = arcpy.MinimumBoundingGeometry_management
            mbe(self.f, "m_out", "ENVELOPE", "LIST", self.field, True)
            print("Complete MinimumBoundingGeometry")
            arcpy.Delete_management(self.f,"FeatureClass")#▶注释3◀
            arcpy.Rename_management("m_out",self.f,"FeatureClass")
            
        if not check_field(self.f,"PAGESIZE"): #▶注释4◀
            # 没有计算过最小几何边界
            print('Add field PAGESIZE')
            arcpy.AddField_management(
                self.f, "PAGESIZE", "TEXT", field_length = 100)
    
    def check_width_height(self): #▶注释1◀
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
        #▶注释2◀
        cursor2l_1 , cursor2l_2 = cursor2l[::5], cursor2l[1::5]
        height_info = {}
        for i in xrange(len(cursor2l_1)): #▶注释3◀
            height = cursor2l_2[i][1] - cursor2l_1[i][1]
            height_info[cursor2l_2[i][0]] = abs(height)
        return height_info

    #▶注释4◀
    def update_width_height(self, height_infomation):
        """
        该方法将 "MBG_Width","MBG_Length"两字段更新为宽和高
        :param height_infomation: {Dict} 包含了制图单位的高度信息
        :return:
        """
        _field = [self.field,"MBG_Width", "MBG_Length"]
        with arcpy.da.UpdateCursor(self.f, _field) as cursor:
            for row in cursor:
                name, width, height = row
                #▶注释5◀
                if round(height_infomation[name], 2) == round(width, 2):
                    row[1] = height
                    row[2] = width
                cursor.updateRow(row)
        print("update width&height completly!")


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
                    #▶注释8◀
                    row[2] = "{}x{}".format(p_size[0],p_size[1])
                else:
                    print("存在超出所有模板页面大小的制图单位")
                cursor.updateRow(row)
        print("update PAGESIZE completly!")


if __name__ == '__main__':
    mxd_d = size_creator(mxd_template)
    PageSizeMatch(MI, FIELD, mxd_d)
