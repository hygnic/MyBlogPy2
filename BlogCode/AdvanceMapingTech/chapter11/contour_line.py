# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/1/9 22:51
# Reference:
"""
Description: 复杂的多边形（内部环岛孔洞等）在显示轮廓线时显得非常的乱和臃肿；本工具的
            作用就是仅仅在
            复杂多边形的外部生成轮廓。
            该方法生成的轮廓线较原始的美观
Usage:
"""
# ---------------------------------------------------------------------------
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import os
import arcpy



class InitPath(object):
    """初始化工作空间，创建gdb数据（如果没有）"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            # if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance
    def __init__(self):
        """_________________________create folder____________________________"""
        scratch_path = "D:\doc\Scratch"
        try:
            if not os.path.isdir(scratch_path):
                os.makedirs(scratch_path)
        except:
            scratch_path = "E:\doc\Scratch"
            if not os.path.isdir(scratch_path):
                os.makedirs(scratch_path)
        """_________________________create folder____________________________"""
        # make gdb
        scratch_gdb = os.path.join(scratch_path, "Scratch.gdb")
        if not arcpy.Exists(scratch_gdb):
            arcpy.CreateFileGDB_management(scratch_path, "Scratch")
        arcpy.env.workspace = scratch_path

        self.scratch_path = scratch_path
        self.scratch_gdb = scratch_gdb

    def __iter__(self):
        return(i for i in (self.scratch_path, self.scratch_gdb))


def merger_all(layer, outputclass= "in_memory/diss_all"):
    """
    一键快速合并一个图层的所有要素(添加一个字段，全部赋值为1，然后融合，最后删除
    该字段)
        <特别注意新合成的图层名称，是否会覆盖>
    layer(String): shp或者lyr文件地址，或者图层对象
    return: 合并后的新图层 默认返回图层名字为 newlayer_945
    """
    arcpy.env.addOutputsToMap = True
    arcpy.env.overwriteOutput = True
    # 判断是否有这个字段
    all_fields = arcpy.ListFields(layer)
    all_name = [i.name for i in all_fields]
    name = "test1f2lcc"
    if name not in all_name:
        arcpy.AddField_management(layer, name, "LONG")
    cursor = arcpy.da.UpdateCursor(layer, name)
    for row in cursor:
        row[0] = "1"
        cursor.updateRow(row)
    del cursor
    new_ly = outputclass
    arcpy.Dissolve_management(layer, new_ly ,name)
    arcpy.DeleteField_management(new_ly, name)
    return new_ly


def better_contour(inputclass, outputclass):
    print("inputclass", inputclass)
    print("outputclass", outputclass)
    arcpy.Merge_management(inputclass, "in_memory/after_merge")
    merger_all("in_memory/after_merge", "in_memory/after_diss_all")
    arcpy.Delete_management("in_memory/after_merge")
    print("merge all")
    arcpy.EliminatePolygonPart_management("in_memory/after_diss_all",
                                          "in_memory/after_eli",
                                          "AREA",
                                          1000000,
                                          part_option="CONTAINED_ONLY" )
    arcpy.Delete_management("in_memory/after_diss_all")
    print("create contour")
    arcpy.SimplifyPolygon_cartography("in_memory/after_eli",
                                      outputclass, algorithm="POINT_REMOVE",
                                      tolerance = 1, error_option="NO_CHECK" ,
                                      collapsed_point_option="NO_KEEP")
    print("complete")


if __name__ == '__main__':
    workpath, workgdb = InitPath()
    arcpy.env.workspace = workgdb
    arcpy.env.overwriteOutput = True
    
    better_contour([ur"G:\MoveOn\mapping\v103\base.gdb\GBZ"], "new_contour_line")

