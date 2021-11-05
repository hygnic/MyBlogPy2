# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              调用exe
# Author:            Hygnic
# Created on:        2021/10/28 12:12
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import subprocess

pname = r"RVT_2.2.1_Win64.exe"

p =subprocess.Popen(pname, stdin=subprocess.PIPE, stdout=subprocess.PIPE)