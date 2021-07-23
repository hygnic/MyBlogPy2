# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/4/18 18:00
# Reference:
"""
Description:
Usage:  HexagonPolygons: <AOI> <Output_Hexagonal_Polygons> <Height_of_Hexagon>
"""
# ---------------------------------------------------------------------------
from __future__ import absolute_import
from __future__ import unicode_literals
import os
import arcpy
import math


class HexPolygon(object):
    
    def __init__(self, in_f, out_f, width=100):
        """
        创建镶嵌六边形
        :param in_f: 输入要素
        :param out_f: 输出要素
        :param width: 六边形的宽,注意不是边长
        """
        self.in_f = in_f
        self.out_f = out_f
        self.width = float(width)

        descinput = arcpy.Describe(self.in_f)
        # if descinput.dataType == "FeatureLayer":
        #     print "FeatureLayer"
        #     inputAreaOfInterest = descinput.CatalogPath # 数据路径
        # else:
        #     print "Not FeatureLayer"
        #     inputAreaOfInterest = self.in_f

        # print inputAreaOfInterest # Hexagon_test.shp
        self.ref = arcpy.Describe(self.in_f).spatialReference
        
        
        #___Function___
        result = self.cal_extent()
        self.create_flow(*result)
    
    
    def cal_extent(self):
        """
        计算出两幅渔网的坐标信息
        :return: 返回两幅渔网矢量的信息
        """
        
        desc = arcpy.Describe(self.in_f)
        
        ext = desc.extent
        x_min = ext.XMin
        x_max = ext.XMax
        y_min = ext.YMin
        y_max = ext.YMax
        
        # calculate offset value

        self.height = self.width * math.sqrt(3)

        self.width, self.height = self.height, self.width

        # Calculate new offset origin, opposite corner and
        # Y axis point coordinates
        factor1 = -2.0
        origin_x = x_min + self.width * factor1
        origin_y = y_min + self.height * factor1
        origin = str(origin_x) + " " + str(origin_y)
        
        # The opposite corner of the fishnet set
        factor2 = 2.0
        corner_coordx = x_max + self.width * factor2
        corner_coordy = y_max + self.height * factor2
        corner_coord=str(corner_coordx) + " " +str(corner_coordy)
        # 新原点
        # global factor3
        factor3 = 0.5
        new_origin_x = str(origin_x + self.width * factor3)
        new_origin_y = str(origin_y + self.height * factor3)
        new_origin = new_origin_x + " " + new_origin_y
        # new opposite corner
        corner_coordx2 = str(corner_coordx + self.width * factor3)
        corner_coordy2 = str(corner_coordy + self.height * factor3)
        corner_coord2 = corner_coordx2 + " " + corner_coordy2
        # note: 使用的是 str
        y_coord1 = str(origin_x) + " " + str(corner_coordy)
        y_coord2 = new_origin_x + " " + corner_coordy2
        
        # Calculate Length, hexagonal area and number of columns
        hexg_len =  float(self.height) / math.sqrt(3)
        # 等边六边形面积计算公式：根号3 * 3 / 2 * 边长 * 边长
        hexg_area = math.sqrt(3)*3/2*pow(hexg_len, 2)
        arcpy.AddMessage("One Hexagon Cell Area: " + str(hexg_area))
        
        vector1 = (origin, y_coord1, corner_coord)
        vector2 = (new_origin, y_coord2, corner_coord2)
        
        return vector1, vector2
        
    
    def create_flow(self, vector1, vector2):
        """
        开始创建六边形
        :param vector1: 用于创建渔网的坐标数据
        :param vector2: 另一个用于创建渔网的坐标数据
        :return:
        """
        
        workspace = os.path.dirname(self.out_f)
        # print os.path.dirname(self.out_f)
        arcpy.env.scratchWorkspace = workspace
        # arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True

        #------ first fishnet ------
        # fishnet1_point -> fishnet1_p point
        # fishnet1_result -> fishnet1_res
        # fishnet1_label -> fishnet1_lb
        CF = arcpy.CreateFishnet_management
        fishnet1_path = (os.path.join(workspace, "Fishnet1"))
        
        fishnet1 = CF(fishnet1_path, vector1[0], vector1[1],
                      self.width, self.height, "0", "0",
                      vector1[2],"LABELS")
        
        #------ second fishnet ------
        fishnet2_path = (os.path.join(workspace, "Fishnet2"))
        
        fishnet2 = CF(fishnet2_path, vector2[0], vector2[1],
                      self.width, self.height, "0", "0",
                      vector2[2], "LABELS")
        
        # label point
        fishnet1_lb = fishnet1.getOutput(1)
        fishnet2_lb = fishnet2.getOutput(1)
        arcpy.DefineProjection_management(fishnet1_lb, self.ref)
        arcpy.DefineProjection_management(fishnet2_lb, self.ref)
        
        # 将新旧标注点（label）合并
        # global full_pt
        full_pt = arcpy.Append_management(fishnet2_lb, fishnet1_lb)
        
        # Create Thiessen Polygons
        full_theissen = arcpy.CreateThiessenPolygons_analysis(
            full_pt,(os.path.join(workspace, "FullTheissen")))
        # 1.将完整的泰森多边形创建为要素图层
        # 2.按位置选择出和输入目标图层相交的部分
        # 3.导出要素图层
        f_lyr = "_lyr"
        arcpy.MakeFeatureLayer_management(full_theissen,f_lyr)
        arcpy.SelectLayerByLocation_management(
            f_lyr,"INTERSECT", self.in_f)
        arcpy.CopyFeatures_management(f_lyr, self.out_f)

        # Delete intermediate data
        arcpy.Delete_management(fishnet1)
        arcpy.Delete_management(fishnet2)
        # arcpy.Delete_management(fishnet1_lb)
        arcpy.Delete_management(fishnet2_lb)
        arcpy.Delete_management(full_theissen)
        arcpy.Delete_management(f_lyr)

        arcpy.AddMessage("Completed hexagonal polygons.")
        

if __name__ == '__main__':
    
    # script
    # arcpy.env.overwriteOutput = True
    # inputfile = "Hexagon_test.shp"
    # output = r"G:\MoveOn\Gispot\gispot\teminal\result.shp"
    # HexPolygon(inputfile, output, 100)
    
    # toolbox
    arcpy.env.overwriteOutput = True
    argv = tuple(arcpy.GetParameterAsText(i)
             for i in range(arcpy.GetArgumentCount()))
    HexPolygon(*argv)