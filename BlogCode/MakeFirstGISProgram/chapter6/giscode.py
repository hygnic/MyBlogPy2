# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Created on: 2021/1/17 14:53

import arcpy
import os

def main(line_shp): #<<注释1>>
    """
    程序运行主函数
    :param line_shp: 线矢量文件
    :return: None
    """
    arcpy.env.workspace = os.getcwd() #<<注释2>>
    arcpy.env.overwriteOutput = True
    # 线要素转面，生成的面矢量名称为 polygon
    arcpy.FeatureToPolygon_management (line_shp, "polygon.shp")
    print "Create polygon"
    # 给 polygon 图层添加字段
    for name in ["CJQYMC", "CJQYDM", "XJQYMC", "XJQYDM"]:
        arcpy.AddField_management("polygon.shp", name,
                                  "TEXT", field_length = 100)
        print "Add field complete"
    print "Done"