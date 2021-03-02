#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2021/3/1 15:12
# Reference:
"""
Description: 复用制图表达规则
Usage:
"""
# ---------------------------------------------------------------------------
import arcpy
import os
print "current dir: << {} >>".format(os.getcwd())

# mxd = arcpy.mapping.MapDocument("CURRENT")
mxd = arcpy.mapping.MapDocument(u"制图表达.mxd")
df = arcpy.mapping.ListDataFrames(mxd)[0]
# target_lyr = arcpy.mapping.ListLayers(mxd)[0]

representation_name = "repre_test2.lyr"
representation_lyr = arcpy.mapping.Layer(representation_name)

# ...
target_lyr = arcpy.mapping.ListLayers(mxd)[0]
res = arcpy.Describe(target_lyr).children
for _r in res:
    print _r.name  #① # representation_name
    print _r.dataType #②  # RepresentationClass
# ...

# # 删除制图表达后
# arcpy.DropRepresentation_cartography(target_lyr, "representation_name")
#
# s_funcname = arcpy.arcpy.AddRepresentation_cartography
# s_funcname(target_lyr,"representation_name", import_rule_layer=representation_lyr)

arcpy.RefreshActiveView()
arcpy.RefreshTOC()
