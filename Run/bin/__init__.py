# ！/usr/bin/python3
# coding:utf-8
# sys
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
runPath = os.path.split(curPath)[0]
rootPath = os.path.split(runPath)[0]
binPath = os.path.join(runPath, 'bin')
confPath = os.path.join(runPath, 'conf')
corePath = os.path.join(runPath, 'core')
dataPath = os.path.join(rootPath, 'DataBase')
usrPath = os.path.split(rootPath)[0]

sys.path.append(rootPath)
sys.path.append(runPath)
sys.path.append(binPath)
sys.path.append(confPath)
sys.path.append(corePath)
sys.path.append(dataPath)
sys.path.append(usrPath)
