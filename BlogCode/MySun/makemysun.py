#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/3/30 10:46
# Reference:
"""
Description:
Usage:
"""
# ---------------------------------------------------------------------------
from __future__ import absolute_import
import arcpy
import numpy as np
import random

def check_field_exit(field_obj, check_field):
    """
    检查图层是否存在该字段
    :param field_obj: field_obj = arcpy.ListFields(layer)
    :param check_field: field
    :return: {Bolean}
    """
    field_names = [i.name for i in field_obj] # field.aliasName
    return check_field in field_names

def add_field(layer, names, f_type, f_length=None, delete=True):
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
        if not check_field_exit(the_fields, name):
            arcpy.AddField_management(layer, name, f_type, field_length=f_length)
            msg = "Created {0} field success".format(name)
            print msg
        else: # 存在该字段
            if delete:
                arcpy.DeleteField_management (layer, name)
                arcpy.AddField_management(layer, name, f_type, field_length=f_length)
            else:
                print "Field exist"
    
    return layer



def randvalue(input_feature, field, range):
    """
    :param input_feature:
    :param field:
    :param range: (a, b)
    :return:
    """
    # add_field()
    print "rows counts:",arcpy.GetCount_management(input_feature)
    with arcpy.da.UpdateCursor(input_feature, field) as cursor:
        count = 0
        for row in cursor:
            count += 1
            if count < 3510 or count > 28296:
                if random.randint(1,10) > 7:
                    row[0]=random.randint(100, 800)
                else:
                    row[0]=random.gauss(range[0], range[1])
                    
            elif count < 7200 or count > 24782:
                if random.randint(1,10) > 8:
                    row[0]=random.randint(100, 800)
                else:
                    row[0]=random.gauss(range[0], range[1])

            elif count < 10530 or count > 21272:
                if random.randint(1,10) > 9:
                    row[0]=random.randint(100, 800)
                else:
                    row[0]=random.gauss(range[0], range[1])

            else:
                row[0]=random.gauss(range[0], range[1])
                
                # row[0]=random.randint(100, 800)
            # row[0]=random.randint(range[0], range[1])
            cursor.updateRow(row)

def show_normal_distribution():
    import numpy as np
    import matplotlib.pyplot as plt
    import math
    
    
    def normal_distribution(x, mu, sigma):
        return np.exp( -1 * ( (x-mu) ** 2) / ( 2 * (sigma ** 2)) ) / (math.sqrt( 2 * np.pi ) * sigma)
    
    mu, sigma = 500, 100
    x = np.linspace( mu - 6 * sigma, mu + 6 * sigma, 100)
    y = normal_distribution(x, mu, sigma)
    plt.plot(x, y, 'r', label='mu = 0,sigma = 1')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    shp_path = ur"D:\MyProject\makemysun\gdb.gdb\test"
    # randvalue(shp_path, "value",(10,500))
    randvalue(shp_path, "value",(500,100))

    
    
    # re = random.gauss(500,1000)
    # print re