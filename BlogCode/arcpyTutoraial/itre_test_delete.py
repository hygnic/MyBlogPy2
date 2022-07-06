# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              itre_test
# Author:            Hygnic
# Created on:        2021/7/12 16:17
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------


# import relevant ABCs from collections module
# from collections import Iterable, Iterator, Sequence
# >>> #create a sample list and arcpy.da.SearchCursor
# >>> l = [10, 20, 30, 40, 50]
# >>> cursor = arcpy.da.SearchCursor(fc,["OID@", "SHAPE@"])
# >>>
# >>> #look at iteration traits of sample objects
# >>> abcs = (Iterable, Iterator, Sequence)
# >>> [isinstance(l, abc) for abc in abcs][True, False, True]  #Iterable, not Iterator, Sequence
# >>>
# >>> [isinstance(cursor, abc) for abc in abcs][True, True, False]  #Iterable, Iterator, not Sequence>>>
# >>> #look at the types for sample objects and iterators of sample objects
# >>> it_l = iter(l)
# >>> type(l)<type 'list'>
# >>> type(it_l)<type 'listiterator'>
# >>>
# >>> it_cur = iter(cursor)
# >>> type(cursor)<type 'da.SearchCursor'>
# >>> type(it_cur)<type 'da.SearchCursor'>
# >>>
# >>> #look at identify of cursor objects>>>
# id(cursor)262686224>>>
# id(it_cur)262686224
# >>>‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍




# Iterating & Looping

# >>> #create list, attach 2 iterators, and retrieve values by
# >>> #    calling next() and object.next()
# >>> l = [10, 20, 30, 40, 50]
# >>> it_l = iter(l)
# >>> it2_l = iter(l)
# >>> print next(it_l), next(it2_l)10 10
# >>> print it_l.next(), it2_l.next()20 20
# >>>
# >>> #create search cursor, attach 2 iterators, and retrieve values by
# >>> #    calling next and object.next()
# >>> cursor = arcpy.da.SearchCursor(fc, ["OID@", "SHAPE@"])
# >>> it_cur = iter(cursor)
# >>> it2_cur = iter(cursor)
# >>> print next(it_cur), next(it2_cur)(1, <Polyline object at 0x1100fcf0[0x1100ff20]>) (2, <Polyline object at 0x1100fcf0[0x1100ff20]>)
# >>> print it_cur.next(), it2_cur.next()(3, <Polyline object at 0x1100fcf0[0x1100ff20]>) (4, <Polyline object at 0x1100fcf0[0x1100ff20]>)
# >>> print next(cursor)(5, <Polyline object at 0x1100fcf0[0x1100ff20]>)>>>‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍



#222
import arcpy
fc = 'c:/data/base.gdb/well'
fields = ['WELL_ID', 'WELL_TYPE', 'SHAPE@XY']
# For each row print the WELL_ID and WELL_TYPE fields, and the
# the feature's x,y coordinates

# Original example using sequence indexing
with arcpy.da.SearchCursor(fc, fields) as cursor:
    for row in cursor:
        print('{0}, {1}, {2}'.format(row[0], row[1], row[2]))


# Example using manual sequence unpacking
with arcpy.da.SearchCursor(fc, fields) as cursor:
    for row in cursor:
        well_id = row[0]
        well_type = row[1]
        well_xy = row[2]
        print('{0}, {1}, {2}'.format(well_id, well_type, well_xy))


# Example using built-in sequence unpacking
with arcpy.da.SearchCursor(fc, fields) as cursor:
    for well_id, well_type, well_xy in cursor:
        print('{0}, {1}, {2}'.format(well_id, well_type, well_xy))‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍
        
        
#Python Built-ins & Itertools

# >>> # Example 1: Get record count using ArcGIS geoprocessing tool
#>>> arcpy.GetCount_management(layer)<Result '52'>>>
# >>>>
# Example 2: Get record count using variable as counter
# >>> with cursor:...     i = 0...     for row in cursor:...         i = i + 1   # or i += 1...     print i...52
# >>>
# >>> # Example 3: Get record count using built-in list and len functions
# >>> with cursor:...
# print len(list(cursor))...52
# >>>
# >>> # Example 4: Get record count using built-in sum function
# >>> with cursor:...
# print sum(1 for row in cursor)...52
# >>>‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍


# 2222
# Retrieve table name for data source of layer
# >>> desc = arcpy.Describe(layer)
# >>> fc_name = desc.featureClass.baseName
# >>>
# >>> # Example 5: Get maximum population record using ArcGIS geoprocessing tools
# >>> summary_table = arcpy.Statistics_analysis(layer,...  "in_memory/summary_max",...    "POP2010 MAX")...
# >>> arcpy.AddJoin_management(layer,...   "POP2010",...  summary_table,...  "MAX_POP2010",...  "KEEP_COMMON")...
# >>> joined_fields = [(field if "@" in field else ".".join([fc_name, field]))...   for field...   in fields
# >>> cursor_sql_join = arcpy.da.SearchCursor(layer, joined_fields)
# >>> print next(cursor_sql_join)(u'CA', 41.639274447708424, u'Pacific', 37253956)
# >>> del cursor_sql_join
# >>> arcpy.RemoveJoin_management(layer, "summary_max")<Result 'USA States\\USA States (below 1:3m)'>
# >>>
# >>> # Example 6: Get maximum population record using SQL subquery
# >>> sql = "POP2010 IN ((SELECT MAX(POP2010) FROM {}))".format(fc_name)
# >>> cursor_sql_subqry = arcpy.da.SearchCursor(layer, fields, sql)
# >>> print next(cursor_sql_subqry)(u'CA', 41.639274447708424, u'Pacific', 37253956)
# >>> del cursor_sql_subqry
# >>>
# >>> # Example 7: Get maximum population record by looping and comparing
# >>> with cursor:...     max_row = next(cursor)...     for row in cursor:...     if row[3] > max_row[3]:...     max_row = row...
# >>> print max_row(u'CA', 41.639274447708424, u'Pacific', 37253956)
# >>>
# >>> # Example 8: Get maximum population record using built-in max function
# >>> from operator import itemgetter
# >>> with cursor:...     print max(cursor, key=itemgetter(3))...(u'CA', 41.639274447708424, u'Pacific', 37253956)
# >>>‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍

# 33333

# Example 9: Print State and population by descending population
# >>> #            using Sort geoprocessing tool
# >>> sorted_table = arcpy.Sort_management(layer,...   "in_memory/sorted_pop",...   "POP2010 DESCENDING")...
# >>> cursor_sorted_table = arcpy.da.SearchCursor(sorted_table, fields)
# >>> with cursor_sorted_table:...   for state, area, sub_region, pop2010 in cursor_sorted_table:...  print "{}, {}".format(state, pop2010)...
    # CA, 37253956TX, 25145561NY, 19378102...DC, 601723WY, 563626PR, -99
# >>> del cursor_sorted_table
# >>>
# >>> # Example 10: Print State and population by descending population
# >>> appending SQL ORDER BY clause
# >>> sql = "ORDER BY POP2010 DESC"
# >>> cursor_orderby_sql = arcpy.da.SearchCursor(layer, fields, sql_clause=(None, sql))
# >>> with cursor_orderby_sql:...     for state, area, sub_region, pop2010 in cursor_orderby_sql:...     print "{}, {}".format(state, pop2010)...
    # CA, 37253956TX, 25145561NY, 19378102...DC, 601723WY, 563626PR, -99
# >>> del cursor_orderby_sql
# >>>
# >>> # Example 11: Print State and population by descending population
# >>> #             using built-in sorted function
# >>> with cursor:...
    # for state, area, sub_region, pop2010 in sorted(cursor,... key=itemgetter(3),...   reverse=True):...  print "{}, {}".format(state, pop2010)...
    # CA, 37253956TX, 25145561NY, 19378102....DC, 601723WY, 563626PR, -99
# >>>‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍