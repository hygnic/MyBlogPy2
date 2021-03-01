# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# arcgis 10.3
# Author: hygnic lcc
# Created on: 2020/4/8 16:33
# Reference:

"""
Description: 将国土土地报备坐标txt文本处理生成shp文件
原始数据如下：
   [属性描述]
   格式版本号=
   数据产生单位=
   数据产生日期=2077
   坐标系=2000ff
   几度分带=
   投影类型=高斯克吕格
   计量单位=米
   带号=ffff
   精度=ffff
   转换参数=fffffff
   [地块坐标]
   41,0,1,0,面,0,0,,@
  - J1,1,3.0, 8.0
   J2,1,1.0, 8.0
   J3,1,2.0, 10.0
   J4,1,3.0, 8.0
   555,0,1,0,面,0,0,,@
   J1,1,9.0, 11.0
   J2,1,9.0, 8.0
   J3,1,6.0, 8.0
   J4,1,6.0, 11.0
   J1,2,7.0, 10.0
  -    J2,2,7.0, 9.0
  -    J3,2,8.0, 9.0
  -    J4,2,8.0, 10.0

处理为如下列表：
       [
            [
            [3.0, 8.0],
            [1.0, 8.0],
            [2.0, 10.0],
            [3.0, 8.0]
            ]
            ,
            [
            [9.0, 11.0],
            [9.0, 8.0],
            [6.0, 8.0],
            [6.0, 11.0],
            [9.0, 11.0]
            ]
            ,
            [
            [7.0, 10.0],
            [7.0, 9.0],
            [8.0, 9.0],
            [8.0, 10.0],
            [7.0, 10.0]
            ]
       ]
每一个会闭合的线都组成一个单独的列表，防止因为首尾不接导致闭合面错误
Usage:
"""
# ---------------------------------------------------------------------------
import re
import arcpy
import os


def points_genarator(txt_file):
	"""
	points_genarator(txt_file)   return list
	txt_file：文本文件地址
	将txt转换为可以使用的点集列表
	"""
	fffs = open(txt_file, "r")
	input_data = fffs.readlines()
	# input_data.remove("\n")
	# 去除换行符
	# input_data = [x.strip() for x in input_data]
	# input_data = input_data[2:]  # 去除前13行
	input_data = [x.strip() for x in input_data if "@" not in x]  # 去除带@的行
	# 去除非J行
	while True:  # 去除前13行
		# 如果首行字符不在下列元组中
		first = ("J", "1", "0", "2", "3", "4", "5", "6", "7", "8", "9")
		if input_data[0][0] not in first:
			del input_data[0]
		# elif :
		#  del input_data[0]
		else:
			break
	# input_data = input_data[12:]  # 去除前13行
	fffs.close()
	# 每一根闭合线单独组成一个列表
	line_closed = []
	# 多根线条组成面
	polygon_list = []
	while input_data:
		row = input_data.pop(0)
		row1 = row.split(",")  # ['J1', '1', '3405133.8969', '35353662.0113']
		# 去除字母和数字组合中的字母 如 "J1" 只保留 "1"
		row_num = re.findall(r'[0-9]+|[a-z]+', row1[0])  # ['1']
		row_num2 = row1[1]  # '1'
		if not line_closed:  # 为空时
			line_closed.append(row1)
			flag1 = int(row_num[0])  # 1 第一列数字
			# 第二列数字
			flag2 = row1[1]  # '1'
		elif int(row_num[0]) > flag1:
			if row_num2 != flag2:  # 第二列出现不一样的，新一轮开始
				flag2 = row_num2
				polygon_list.append(line_closed)
				line_closed = []
			# 未开始新一轮就接着上一个，如果开始新一轮那么这里就是第一个起始点
			line_closed.append(row1)
		elif int(row_num[0]) == flag1:  # 新一轮开始
			polygon_list.append(line_closed)
			line_closed = []
			line_closed.append(row1)
	if line_closed:
		polygon_list.append(line_closed)
	return polygon_list


def draw_poly(coord_list, sr, y, x):
	"""
	创建多边形
	coord_list(List)：多个点组成的坐标
	sr: 投影系
	y(Int): y坐标列
	x(Int): x坐标列
	"""
	parts = arcpy.Array()
	yuans = arcpy.Array()
	yuan = arcpy.Array()
	for part in coord_list:
		for pnt in part:
			if pnt:
				yuan.add(arcpy.Point(pnt[y], pnt[x]))
			else:
				# null point - we are at the start of a new ring
				yuans.add(yuan)
				yuan.removeAll()
		# we have our last ring, add it
		yuans.add(yuan)
		yuan.removeAll()
		# if we only have one ring: remove nesting
		if len(yuans) == 1:
			yuans = yuans.getObject(0)
		parts.add(yuans)
		yuans.removeAll()
	# 只有一个，单个图形
	if len(parts) == 1:
		parts = parts.getObject(0)
	return arcpy.Polygon(parts, sr)


def main(info, txt_folder, output_folder):
	"""
	功能实现的主函数
	bubbletip(List): 存放信息的列表，作为独立脚本使用时没啥用
	txt_folder(Unicode/String): 包含txt文件的文件夹
	output_folder(Unicode/String): 导出文件夹
	"""
	arcpy.env.overwriteOutput = True
	txts = os.listdir(txt_folder)
	for txt in txts:
		if txt[-3:].lower() == "txt":
			txt_p = os.path.join(txt_folder, txt)
			f = points_genarator(txt_p)
			name = os.path.splitext(os.path.basename(txt_p))[0]  # 获取名称不带后缀
			# 创建空白shp
			blank_shp = arcpy.CreateFeatureclass_management(output_folder,
															name, "Polygon",
															spatial_reference=None)
			# create the polygons and write them
			Rows = arcpy.da.InsertCursor(blank_shp, "SHAPE@")
			
			p = draw_poly(f, sr=None, y=3, x=2)
			
			Rows.insertRow([p])
			del Rows
			write_sth = "Write done: " + os.path.join(output_folder,
													  name)
			print write_sth
			info.append(write_sth)
			
			# 给新建的shp文件添加 MC 字段和值
			shp_name = name + ".shp"
			newfield_name = "MC"
			fresh_layer = arcpy.mapping.Layer(
				os.path.join(output_folder, shp_name))
			arcpy.AddField_management(fresh_layer, newfield_name, "TEXT",
									  field_length=100)
			cursor2 = arcpy.da.UpdateCursor(fresh_layer, newfield_name)
			for roww in cursor2:
				roww[0] = name
				cursor2.updateRow(roww)
			del cursor2


if __name__ == '__main__':
	"""脚本单独使用"""
	"""---------------------------------------------------------------"""
	"""------------------------PARA-----------------------------------"""
	arcpy.env.overwriteOutput = True
	dir_p = ur"G:\高标准分布图\金堂县\txt"  # txt文件夹
	output_dir = ur"G:\高标准分布图\金堂县\新建文件夹"  # 输出文件夹
	"""---------------------------------------------------------------"""
	"""---------------------------------------------------------------"""
	infos = []
	main(infos, dir_p, output_dir)