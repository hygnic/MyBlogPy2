# -*- coding:CP936 -*-
# -------------------------------------------
# Name:              better_isogram
# Author:            Hygnic
# Created on:        2021/9/16 11:09
# Version:           
# Reference:         
"""
Description:       更好的等值线
Usage:               
"""
# -------------------------------------------
from __future__ import absolute_import
import arcpy
import os
from random import randint



def better_isogram(input_raster, neighborhood, distance, base_contour, output):
    """
    直接使用软件自带的等值线工具制作栅格的等值线，
    线条比较曲折同时较为零碎，不利于解译；
    集成焦点统计工具对原始栅格数据处理后再生产等值线图，
    线条清晰光滑，易于解译和使用。
    :param input_raster: 输入栅格
    :param neighborhood: {Int} 邻域分析，指定的像元范围
    :param distance: {Double} 等值线间隔
    :param base_contour: {Double} 起始等值线值 默认值为零
    :param output: 输出
    :return:
    """
    arcpy.env.workspace = os.path.dirname(input_raster)
    
    # 进行焦点统计分析
    
    fs = arcpy.sa.FocalStatistics
    nrt = arcpy.sa.NbrRectangle
    neighborhood = int(neighborhood)
    neighborhood = nrt(neighborhood, neighborhood, "cell")
    fs_result = fs(input_raster, neighborhood, "MEAN")
    # name_random = randint(0,99999)
    # fs_name = "temp{}".format(name_random)
    # fs_result.save(fs_name)
    arcpy.AddMessage("FocalStatistics Done")
    # 等值线计算
    contour = "in_memory/contour"
    # arcpy.sa.Contour(fs_result, contour, float(distance))
    arcpy.sa.Contour(fs_result, output, float(distance), float(base_contour))
    arcpy.AddMessage("Contour Done")
    # arcpy.Delete_management(fs_name)
    
    
    # 下面为啥要擦除我记不清了，但是经我测试，擦布擦除效果都一样 20231017
    # 获得输入栅格范围矢量
    # 其实这里可以使用栅格转面工具 arcpy.conversion.RasterToPolygon
    # 不过前提是使用栅格计算器让栅格乘以0

    # domain = "in_memory/domain"
    # arcpy.RasterDomain_3d(input_raster, domain, "POLYGON")
    # arcpy.AddMessage("Boundary Get Done")
    # # 擦除范围外的线条
    #
    # name_random = randint(0,99999)
    # erase_left = "%scratchFolder%/out{}.shp".format(name_random)
    # # arcpy.AddMessage(neighborhood)
    # arcpy.Erase_analysis(contour, domain, erase_left)
    # # arcpy.AddMessage(neighborhood)
    # try:
    #     arcpy.Erase_analysis(contour, erase_left, output)
    # except Exception as e:
    #     print "error"
    # arcpy.Delete_management(erase_left)


if __name__ == '__main__':
    mark = 0 #=1表示测试
    arcpy.env.overwriteOutput = True
    
    if mark != 1:
        arcpy.AddMessage("\n|---------------------------------|")
        arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ------")
        arcpy.AddMessage("|---------------------------------|\n")
        
        args = tuple(
            arcpy.GetParameterAsText(i) for i in range(
                arcpy.GetArgumentCount()))
        better_isogram(*args)
    else:
        in_1 = r"D:\BaiduSyncdisk\3.RasterData\1.ProjectDB\14制图南海区域\制图南海区域.gdb\GEBCO_Area_3857underwater1"
        in_2 = 7
        in_3 = 100
        in_4 = 0
        in_5 = r"D:\BaiduSyncdisk\3.RasterData\1.ProjectDB\14制图南海区域\制图南海区域.gdb\Cont_100"
        
        better_isogram(in_1,in_2,in_3,in_4, in_5)
        
        