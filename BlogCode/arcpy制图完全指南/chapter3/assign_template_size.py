#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/1/29 17:34
# Reference:
"""
Description: 分配模板大小
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


def size_creator(path):
    """
    根据输入的模板文件地址生成标准格式的字典。
    :param path: {String} mxd file path
    :return: {Dict} such as: {'pagesize3': (1180, 900), 'pagesize2': (1080, 700), 'pagesize1': (1080, 1300)}
    """
    print("请确保模板文件夹中不存在无关文件！")
    m_dict = {}
    counter = 1
    for mxd_name in [os.path.splitext(x)[0] for x in os.listdir(path) if ".mxd" or ".MXD" in x]:
        # print(mxd_name) # 1080x1300
        width, height = mxd_name.split("x")
        name = "pagesize{}".format(counter)
        m_dict[name] = (int(width), int(height))
        counter+=1
    # {
    #     "pagesize1":(1080,700),
    #     "pagesize2":(1080,1300),
    #     "pagesize3":(1180,900)
    # }
    return m_dict


def select_template_size(size, template_size):
    """
    根据给出的size大小去 template_size字典中匹配大小合适的模板，然后返回名称，如 pagesize3
    :param size:  宽和高组成的列表 such as:[659.8490915000066, 822.3146429999917]
    :param template_size: 制图模板大小
    :return: 返回制图模板大小的名称（键），如果找不到适合的制图模板就返回 -1
    """
    map_w, map_h = size[0], size[1]
    map_div = map_w/map_h
    # 符合该制图单位的模板大小的字典
    template_size_fit = {k:(v[0], v[1], v[0]*v[1], v[0]/v[1]) for k,v in template_size.items() if v[0]>map_w and v[1]>map_h}
    d_len = len(template_size_fit)
    d2l = zip(template_size_fit.keys(), template_size_fit.values()) # 字典转列表
    d2l_sorted = sorted(d2l, key=lambda x: x[1][2]) # 按元组中第三个数大小排序（按面积大小）
    if d_len > 2:
        two_remaind = d2l_sorted[:2]
        # print(two_remaind)
        res = min(two_remaind, key=lambda x: abs(x[1][3]-map_div)) # (u'pagesize3', (1380, 850, 1173000, 1.6235294117647059))
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
        :param mxd_template_d: {Dict} 装有模板大小的字典
        """
        self.f = feature_name # 制图索引图层的名字
        self.field = field
        self.m_d = mxd_template_d
        self.minimum_bounding() # 制作最小几何边界图层
        true_height = self.check_width_height() # 获取真实的高度信息
        self.update_width_height(true_height) # 将高度信息更新入制图索引图层（MappingIndex）
        self.update_page_size(SCALE)
    
    def minimum_bounding(self):
        """
        1.计算最小边界几何，并用结果图层覆盖初始图层;计算过最小边界几何的图层有"MBG_Width"字段
        2.创建PAGRSIZE 字段
        :return: 制图索引文件的要素图层
        """
        if not check_field(MI,"MBG_Width"): # 没有计算过最小几何边界
            short_f = arcpy.MinimumBoundingGeometry_management
            short_f(self.f, "mapping_index_out", "ENVELOPE", "LIST", self.field, True)
            print("create MinimumBoundingGeometry")
            arcpy.Delete_management(self.f, "FeatureClass")
            arcpy.Rename_management("mapping_index_out", self.f, "FeatureClass")
        if not check_field(self.f,"PAGESIZE"): # 没有计算过最小几何边界
            print('ceate Field "PAGESIZE"')
            arcpy.AddField_management(self.f, "PAGESIZE", "TEXT", field_length = 100)
    
    def check_width_height(self):
        # 使用 “要素折点转点要素” 工具，将最小几何边界转变成点；
        # 每一个最小几何边界都会生成5个点：左下，左上，右上，右下，左下；
        # 前两个点的差值就是高度
        # 返回值为高度的字典：{地级市名称：高度}
            # {..."广安市":879.2, "巴中市":124.56, "桂林市":54.7801, ...}
        feature_vertices = "feature_vertices" # feature name
        short_f = arcpy.FeatureVerticesToPoints_management
        short_f(self.f, feature_vertices, "ALL")
        cursor = arcpy.da.SearchCursor(feature_vertices, [self.field, "SHAPE@Y"])
        cursor2l = [(x[0],x[1]) for x in cursor] # 转换成列表
        del cursor
        cursor2l_1 , cursor2l_2 = cursor2l[::5], cursor2l[1::5]  # [(u'\u5df4\u4e2d\u5e02', 3460475.693600001), (u'\u5df4\u4e2d\u5e02', 3331847.4146)]
        height_info = {}
        for i in xrange(len(cursor2l_1)):
            height = cursor2l_2[i][1] - cursor2l_1[i][1]
            height_info[cursor2l_2[i][0]] = abs(height)
        return height_info
    
    
    def update_width_height(self, height_infomation):
        """
        最小边界几何的"MBG_Width", "MBG_Length"两字段，不是宽和高的关系，二是短边和长边的关系；
        这样的话，横卧状和长条状无法区分；
        该方法将 "MBG_Width", "MBG_Length"两字段的关系更新为宽和高。这样就能区分横卧和长条状。
        :param height_infomation: {Dict} 包含了制图单位的高度信息
        :return:
        """
        with arcpy.da.UpdateCursor(self.f, [self.field,"MBG_Width", "MBG_Length"]) as cursor:
            for row in cursor:
                name, width, height = row
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
        with arcpy.da.UpdateCursor(self.f, ["MBG_Width", "MBG_Length", "PAGESIZE"]) as cursor:
            for row in cursor:
                row_p = [row[0], row[1]]
                # print("row_p:",row_p)
                new_row = [x/scale*1000 for x in row_p] # 单位换算成了毫米 mm [659.8490915000066, 822.3146429999917]
                # print("new_row:",new_row)
                page_size_name = select_template_size(new_row, self.m_d) # PAGESIZE1 or -1
                if page_size_name != -1:
                    p_size = self.m_d[page_size_name] # (1180, 900)
                    # update PAGESIZE field values
                    row[2] = "{}x{}".format(p_size[0],p_size[1]) # 1180x900
                    # print(res)
                else:
                    print("存在超出所有模板页面大小的制图单位")
                cursor.updateRow(row)
        print("update PAGESIZE completly!")


if __name__ == '__main__':
    mxd_d = size_creator(mxd_template)
    PageSizeMatch(MI, FIELD, mxd_d)
