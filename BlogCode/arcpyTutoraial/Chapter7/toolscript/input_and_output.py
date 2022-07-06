# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              input_and_output
# Author:            Hygnic
# Created on:        2021/12/2 16:54
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy

# 第一种写法

# input_lyr = arcpy.GetParameterAsText(0)
# output = arcpy.GetParameterAsText(1)
#
#
# if __name__ == '__main__':
#     lyr = arcpy.mapping.Layer(input_lyr)
#     arcpy.CopyFeatures_management(lyr, output)



# 第二种写法

def in_and_out(in_lyr, out_lyr):
    lyr = arcpy.mapping.Layer(in_lyr)
    arcpy.AddMessage("Hello World")
    arcpy.CopyFeatures_management(lyr, out_lyr)


if __name__ == '__main__':
    
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    in_and_out(*argv)