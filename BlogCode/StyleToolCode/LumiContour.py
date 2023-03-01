# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              LumiContour
# Author:            Hygnic
# Created on:        2021/5/31 12:46
# Version:           
# Reference:         
"""
Description:         发光轮廓 9级缓冲，同一种颜色，不过透明度
                     依次降低
                     使用 opacity.lyr
                     已经导入工具箱 <<发光轮廓>>
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import sys
from random import randint



class OpacityContour(object):
    # 创建透明渐变的外边缘。
    # 1.先创建9层缓冲区
    # 2.新建字段用于存放不同级别缓冲区的透明度
    
    def __init__(self, in_f, times, lyr, output):
        """
        :param in_f: 输入要素
        :param times: 放大倍数
        :param lyr: lyr 效果图层
        :param output: 样式图层输出
        """
        self.mxd = arcpy.mapping.MapDocument("CURRENT")
        self.df = arcpy.mapping.ListDataFrames(self.mxd)[0]
        
        self.in_f = in_f
        self.times = times
        self.lyr = arcpy.mapping.Layer(lyr)
        self.output = output
        
        self.distance = [i*10 for i in xrange(1, 10)]
        
        self.make_buffer_ring()
        self.set_opacity()
        arcpy.Delete_management(self.buffered)

    def make_buffer_ring(self):
        arcpy.AddMessage("Making buffer rings……")
        num = int(self.times)
        inputfile = self.in_f
        distance = [_*num for _ in self.distance]
        # self.buffered = arcpy.CreateScratchName(prefix="buffered", workspace=os.path.join(os.path.dirname(self.output)))
        buffername = "in_memory/ne"+str(randint(1, 10000))
        self.buffered = buffername
        arcpy.MultipleRingBuffer_analysis(inputfile, self.buffered, distance, "Meters", Outside_Polygons_Only=True)
        
        # 将相同距离的缓冲区合并，因为在某些情况下，同一距离的缓冲区可能会变成几个要素
        # Dissolve same distance feature
        arcpy.Dissolve_management(self.buffered, self.output, dissolve_field="distance", statistics_fields="", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")
        # set symbol and add layer to ArcMap
        self.res_lyr = arcpy.mapping.Layer(self.output)
        # self.res_lyr = arcpy.mapping.Layer(inputfile)
        
        
    def set_opacity(self):
        f_name = "opacity"
        arcpy.AddMessage("Apply style setting……")
        # self.add_field(self.res_lyr, [f_name], "SHORT")

        arcpy.AddField_management(self.res_lyr, f_name, "SHORT", field_length="")
        
        with arcpy.da.UpdateCursor(self.res_lyr, f_name) as cursor:
            in_count = 0
            for row in cursor:
                row[0] = self.distance[in_count]
                in_count += 1
                cursor.updateRow(row)
        arcpy.mapping.UpdateLayer(self.df,  self.res_lyr, self.lyr)
        arcpy.mapping.AddLayer(self.df, self.res_lyr)
        arcpy.AddMessage(self.res_lyr.dataSource)

    
if __name__ == '__main__':
    #------------------------------
    #------------path--------------
    #       在导入的情况下
    # arcpy.AddMessage("CURRENT: {}".format(os.getcwd()))
    # CURRENT: C:\Windows\system32

    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ------")
    arcpy.AddMessage("|---------------------------------|\n")


# 返回工具箱的完整名称
    toolbox = os.path.abspath(sys.argv[0])
    tool_dir = os.path.abspath(os.path.dirname(toolbox))
    # lyr
    dir_lyr = os.path.join(tool_dir, "lyr") # StyleTool/lyr
    # 制图表达文件存储位置
    representation = os.path.join(tool_dir, "Representation")
    rp_gdb = os.path.join(representation, "rep_base.gdb")
    #------------path--------------
    #------------------------------
    
    #------------------------------
    #----------workspace-----------
    arcpy.env.workspace = os.path.dirname(arcpy.GetParameterAsText(2))
    work = arcpy.env.workspace
    #----------workspace-----------
    #------------------------------



    # arcpy.env.addOutputsToMap = True
    lyr_file = os.path.join(dir_lyr, "opacity.lyr")
    OpacityContour(arcpy.GetParameterAsText(0),
                   arcpy.GetParameterAsText(1), lyr_file,
                   arcpy.GetParameterAsText(2))