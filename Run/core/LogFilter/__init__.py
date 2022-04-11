import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
corePath = os.path.split(curPath)[0]
runPath = os.path.split(corePath)[0]
rootPath = os.path.split(runPath)[0]
binPath = os.path.join(rootPath, 'bin')
confPath = os.path.join(rootPath, 'conf')


sys.path.append(rootPath)
sys.path.append(runPath)
sys.path.append(binPath)
sys.path.append(confPath)
sys.path.append(corePath)