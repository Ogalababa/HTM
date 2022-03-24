import sys
import os

rootPath = os.path.abspath(os.path.dirname(__file__))
runPath = os.path.join(rootPath, 'Run')
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
sys.path.append(usrPath)
