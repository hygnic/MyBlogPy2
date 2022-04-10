# -*- coding:utf-8 -*-
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

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")


def better_isogram(input_raster, neighborhood, distance, output):
    """
    直接使用软件自带的等值线工具制作栅格的等值线，
    线条比较曲折同时较为零碎，不利于解译；
    集成焦点统计工具对原始栅格数据处理后再生产等值线图，
    线条清晰光滑，易于解译和使用。
    :param input_raster: 输入栅格
    :param output: 输出更好的等值线数据集。
    :param neighborhood: {Int} 邻域分析，指定的像元范围
    :param distance: {Double} 等值线间隔
    :return:
    """
    
    # 进行焦点统计分析
    
    fs = arcpy.sa.FocalStatistics
    nrt = arcpy.sa.NbrRectangle
    neighborhood = int(neighborhood)
    neighborhood = nrt(neighborhood, neighborhood, "cell")
    fs_result = fs(input_raster, neighborhood, "MEAN")
    
    # 等值线计算
    contour = "in_memory/contour"
    arcpy.sa.Contour(fs_result, contour, float(distance))
    
    # 获得输入栅格范围矢量
    domain = "in_memory/domain"
    arcpy.RasterDomain_3d(input_raster, domain, "POLYGON")
    
    # 擦除范围外的线条
    
    erase_left = "%scratchFolder%/out172005.shp"
    # arcpy.AddMessage(neighborhood)
    arcpy.Erase_analysis(contour, domain, erase_left)
    # arcpy.AddMessage(neighborhood)
    arcpy.Erase_analysis(contour, erase_left, output)
    arcpy.Delete_management(erase_left)


if __name__ == '__main__':
    args = tuple(
        arcpy.GetParameterAsText(i) for i in range(
            arcpy.GetArgumentCount()))
    better_isogram(*args)
