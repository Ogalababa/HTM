import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
runPath = os.path.join(rootPath, 'Run')
binPath = os.path.join(runPath, 'bin')
confPath = os.path.join(runPath, 'conf')
corePath = os.path.join(runPath, 'core')

sys.path.append(rootPath)
sys.path.append(runPath)
sys.path.append(binPath)
sys.path.append(confPath)
sys.path.append(corePath)
