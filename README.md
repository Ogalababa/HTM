# 程序简介
HTM 内部程序，主要通过转轨器日志分析转轨器状态的程序

## 环境配置
### 服务器配置
- install software
```bash
sudo apt update

# install pip
sudo apt install python3-pip

# install vim
sudo apt install vim

# install jupyter
sudo apt install jupyterlab

#config jupyterlab
jupyter-lab --generate-config
sudo vim /home/suj/.jupyter_lab_config.py
```
```python3
c.ServerApp.allow_origin = '*'
c.ServerApp.ip = '*'
```

```bash
# install anaconda3
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
sha256sum Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh
source ~/.bashrc

# install streamlit
conda install -c conda-forge streamlit
```
- set jupyter auto start
```bash
cd /
vim /etc/systemd/system/jupyter-lab.service 
```
```bash
#Add to jupyter-lab.service
[Unit]
Description=jupyter-lab
After=network.target
[Service]
Type=simple
# 这里填用户名，下同
User=sky
EnvironmentFile=/home/suj/.local/bin/jupyter-lab
ExecStart=/home/suj/.local/bin/jupyter-lab
ExecStop=/usr/bin/pkill /home/suj/.local/bin/jupyter-lab
KillMode=process
Restart=on-failure
RestartSec=30s
[Install]
WantedBy=multi-user.target

```
```bash
sudo systemctl daemon-reload
sudo systemctl enable jupyter.service
sudo systemctl start jupyter.service
systemctl status jupyter
```

### 依赖库
- Run
  - sqlalchemy
  - tqdm
  - pandas
  - multiprocessing
  - cryptocode
  - configparser
  - re

- Show
  - streamlit
  - plotly
  - fpdf
  - tempfile

## 结构图
flow
st=>start: start
op=>operation: your Operation
cond=>condition: Yes or No?
e=>end
st->op->end


流程图： 从服务器下载log文件=>翻译成自然语言数据=>存到数据库

从数据库查询表=>通过streamlib映射到浏览器

* [X]  配置ini文件，翻译log数据
* [X]  以日期为分割保存到sqlite数据库
* [X]  重写 import ini
* [X]  查询sqlite3数据库
* [X]  设置streamlit页面
* [X]  streamlit 显示 总运行数量， 各个wissel占比 饼图
* [X]  显示 Wissel 一天内高峰运行密度 条形图
* [ ]  显示 Wissel 错误运行数量 个原因占比
* [ ]  配置wissel W6XX系列
* 

