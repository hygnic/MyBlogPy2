# -*- coding:CP936 -*-
# -------------------------------------------
# Name:              better_isogram
# Author:            Hygnic
# Created on:        2021/9/16 11:09
# Version:           
# Reference:         
"""
Description:       ���õĵ�ֵ��
Usage:               
"""
# -------------------------------------------
from __future__ import absolute_import
import arcpy
import os
from random import randint



def better_isogram(input_raster, neighborhood, distance, base_contour, output):
    """
    ֱ��ʹ������Դ��ĵ�ֵ�߹�������դ��ĵ�ֵ�ߣ�
    �����Ƚ�����ͬʱ��Ϊ���飬�����ڽ��룻
    ���ɽ���ͳ�ƹ��߶�ԭʼդ�����ݴ������������ֵ��ͼ��
    ���������⻬�����ڽ����ʹ�á�
    :param input_raster: ����դ��
    :param neighborhood: {Int} ���������ָ������Ԫ��Χ
    :param distance: {Double} ��ֵ�߼��
    :param base_contour: {Double} ��ʼ��ֵ��ֵ Ĭ��ֵΪ��
    :param output: ���
    :return:
    """
    arcpy.env.workspace = os.path.dirname(input_raster)
    
    # ���н���ͳ�Ʒ���
    
    fs = arcpy.sa.FocalStatistics
    nrt = arcpy.sa.NbrRectangle
    neighborhood = int(neighborhood)
    neighborhood = nrt(neighborhood, neighborhood, "cell")
    fs_result = fs(input_raster, neighborhood, "MEAN")
    # name_random = randint(0,99999)
    # fs_name = "temp{}".format(name_random)
    # fs_result.save(fs_name)
    arcpy.AddMessage("FocalStatistics Done")
    # ��ֵ�߼���
    contour = "in_memory/contour"
    # arcpy.sa.Contour(fs_result, contour, float(distance))
    arcpy.sa.Contour(fs_result, output, float(distance), float(base_contour))
    arcpy.AddMessage("Contour Done")
    # arcpy.Delete_management(fs_name)
    
    
    # ����ΪɶҪ�����Ҽǲ����ˣ����Ǿ��Ҳ��ԣ���������Ч����һ�� 20231017
    # �������դ��Χʸ��
    # ��ʵ�������ʹ��դ��ת�湤�� arcpy.conversion.RasterToPolygon
    # ����ǰ����ʹ��դ���������դ�����0

    # domain = "in_memory/domain"
    # arcpy.RasterDomain_3d(input_raster, domain, "POLYGON")
    # arcpy.AddMessage("Boundary Get Done")
    # # ������Χ�������
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
    mark = 0 #=1��ʾ����
    arcpy.env.overwriteOutput = True
    
    if mark != 1:
        arcpy.AddMessage("\n|---------------------------------|")
        arcpy.AddMessage(" -----  ������ GIS�� ����������  ------")
        arcpy.AddMessage("|---------------------------------|\n")
        
        args = tuple(
            arcpy.GetParameterAsText(i) for i in range(
                arcpy.GetArgumentCount()))
        better_isogram(*args)
    else:
        in_1 = r"D:\BaiduSyncdisk\3.RasterData\1.ProjectDB\14��ͼ�Ϻ�����\��ͼ�Ϻ�����.gdb\GEBCO_Area_3857underwater1"
        in_2 = 7
        in_3 = 100
        in_4 = 0
        in_5 = r"D:\BaiduSyncdisk\3.RasterData\1.ProjectDB\14��ͼ�Ϻ�����\��ͼ�Ϻ�����.gdb\Cont_100"
        
        better_isogram(in_1,in_2,in_3,in_4, in_5)
        
        