# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              test_speed
# Author:            Hygnic
# Created on:        2021/8/3 15:32
# Version:           
# Reference:         
"""
Description:         测试mxd导出jpg地图的时间 使用装饰器版本
Usage:               
"""
# -------------------------------------------
import arcpy
from time import time
import os

outpath = os.path.abspath(os.getcwd())


    
def time_counter(func):
    def warp():
        strat_time = time()
        func()
        use_time = time()-strat_time
        print use_time
        
    return warp
        
@time_counter
def sample():
    # time1 = time()
    mxd = arcpy.mapping.MapDocument("CURRENT")
    arcpy.mapping.ExportToJPEG(mxd,
                               os.path.join(outpath, "res"),
                               resolution=300)
    # print time()- time1


if __name__ == '__main__':
    sample()