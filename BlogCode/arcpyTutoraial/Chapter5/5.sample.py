# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              5.sample
# Author:            Hygnic
# Created on:        2021/7/14 21:19
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os

arcpy.env.overwriteOutput = True
wk_path = os.path.abspath("../NYC.gdb")
arcpy.env.workspace = wk_path


# 拆包

# field = ["BoroName", "SHAPE@AREA"]
# with arcpy.da.SearchCursor("Boroughs", field) as cursor:
#     for name, area in cursor: # ▶注释1◀
#         print name


# 惰性释放

field = ["BoroName", "SHAPE@AREA"]
# <<<传统写法>>>
new_list = []
with arcpy.da.SearchCursor("Boroughs", field) as cursor:
    for name, area in cursor:
        new_list.append((name, area))

# 将全部数据装进一个列表
print new_list
del cursor

#　<<<<惰性释放写法>>>
cursor = arcpy.da.SearchCursor("Boroughs", field)
new_list2 = list(cursor)
print new_list2

del cursor


# 获取极值

from operator import itemgetter
field = ["BoroName", "SHAPE@AREA"]
with arcpy.da.SearchCursor("Boroughs", field) as cursor:
    print max(cursor, key=itemgetter(1))

del cursor


# 降序/升序排列

from operator import itemgetter
field = ["BoroName", "SHAPE@AREA"]
with arcpy.da.SearchCursor("Boroughs", field) as cursor:
    for name, area in sorted(cursor,  key=itemgetter(1), reverse=True):
        print (name, area)
    