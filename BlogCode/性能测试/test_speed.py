# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              test_speed
# Author:            Hygnic
# Created on:        2021/8/3 15:32
# Version:
# Reference:
"""
Description:         测试mxd导出jpg地图的时间
Usage:
"""
# -------------------------------------------
import arcpy
from time import time
import os


outpath = os.path.abspath(os.getcwd())

def sample():
    time1 = time()
    mxd = arcpy.mapping.MapDocument("CURRENT")
    arcpy.mapping.ExportToJPEG(mxd,
                               os.path.join(outpath, "res"),
                               resolution=300)
    return time()- time1


if __name__ == '__main__':
    time_list = []
    for i in xrange(10):
        time_list.append(sample())
    print sum(time_list)/len(time_list)