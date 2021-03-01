#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/1/19 16:53
# Reference:
"""
Description:
Usage:
"""
# ---------------------------------------------------------------------------
import arcpy
workspace = ur"E:\doc\Scratch\arcpy指南.gdb"
arcpy.env.workspace = workspace
gen = arcpy.da.Walk(workspace, datatype="FeatureClass")
for dirpath, dirnames, filenames in gen:
    all_filenames = list(filenames)
    
print all_filenames

for name in all_filenames:
    print name
    lst_fields = arcpy.ListFields(name)
    if "CITY" not in lst_fields:
        arcpy.AddField_management(name, "CITY", "TEXT", field_length = 50)
    arcpy.CalculateField_management(name, "CITY", "!NAME_1!", "PYTHON")

