# ！/usr/bin/python3
# coding:utf-8
# sys
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
runPath = os.path.split(curPath)[0]
rootPath = os.path.split(runPath)[0]
binPath = os.path.split(runPath)[0]
confPath = os.path.split(runPath)[0]
corePath = os.path.split(runPath)[0]

sys.path.append(rootPath)
sys.path.append(runPath)
sys.path.append(binPath)
sys.path.append(confPath)
sys.path.append(corePath)
