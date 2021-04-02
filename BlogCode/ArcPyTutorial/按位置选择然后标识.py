#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/4/2 12:22
# Reference:
"""
Description:
Usage:
"""
# ---------------------------------------------------------------------------
import arcpy
import timeit

arcpy.env.workspace=ur"按位置选择然后标识.gdb"
arcpy.env.overwriteOutput = True




def join_attrbute():
    sba = arcpy.SelectLayerByAttribute_management
    
    pac = "PACounties_class"
    pac_fl = "PACounties_class_featurelyr"
    sel_type = "NEW_SELECTION"
    expression = "DLMC = '水田'"
    arcpy.MakeFeatureLayer_management(pac, pac_fl)
    sba(pac_fl, sel_type, expression)
    
    # arcpy.CopyFeatures_management("merge_layer", "merge_layer12312")
    
    identity_dltb = "identity_dltb"
    pac_name = "PACounties"
    arcpy.Identity_analysis(pac_fl, pac_name, identity_dltb)
    print "Completed"
    
print timeit.timeit(join_attrbute, number=10) # 34.928