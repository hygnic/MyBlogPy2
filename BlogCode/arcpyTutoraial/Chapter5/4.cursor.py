# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              4we
# Author:            Hygnic
# Created on:        2021/7/14 20:23
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy
import os
from collections import Iterable, Iterator, Sequence


arcpy.env.overwriteOutput = True
wk_path = os.path.abspath("../NYC.gdb")
arcpy.env.workspace = wk_path


l = [1, 2, 3, 4]
cursor = arcpy.da.SearchCursor("Boroughs", ["OID@", "SHAPE@"])


abcs = (Iterable, Iterator, Sequence)
print [isinstance(l, abc) for abc in abcs]
# [True, False, True]  #Iterable, not Iterator, Sequence

print [isinstance(cursor, abc) for abc in abcs]
# [True, True, False]  #Iterable, Iterator, not Sequence


# 使用内置函数 iter()
it_l = iter(l)
t1 = type(l) # <type 'list'>
t2 = type(it_l) # <type 'listiterator'>

it_cur = iter(cursor)
t3 = type(cursor) # <type 'da.SearchCursor'>
t4 = type(it_cur) # <type 'da.SearchCursor'>

#look at identify of cursor objects
print id(cursor) # 105692320
print id(it_cur) # 105692320