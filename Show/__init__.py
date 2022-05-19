import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
homePath = os.path.split(rootPath)[0]
sys.path.append(curPath)
sys.path.append(rootPath)
sys.path.append(homePath)
