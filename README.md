<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [程序简介](#%E7%A8%8B%E5%BA%8F%E7%AE%80%E4%BB%8B)
  - [环境配置](#%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE)
    - [服务器配置](#%E6%9C%8D%E5%8A%A1%E5%99%A8%E9%85%8D%E7%BD%AE)
    - [依赖库](#%E4%BE%9D%E8%B5%96%E5%BA%93)
  - [结构图](#%E7%BB%93%E6%9E%84%E5%9B%BE)
  - [文件简介](#%E6%96%87%E4%BB%B6%E7%AE%80%E4%BB%8B)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

﻿# 程序简介
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
  ```mermaid
  graph LR

  log[log file] --> rl[read_log]
  rl --> conver_data
  HkConfig --> conver_data
  conver_data --Save to sql--> DataBase
  DataBase --GetData.py--> Show
  Show --streamlit-->brouwser[Show in brouwser]
  
  ```

## 文件简介

- HkConfig.Config.py
  - line_to_hex: 读取log文件,分割hex代码到列表
  - list_to_str: 拼接列表中hex代码
  - hex_to_bin： hex代码转二进制代码
  - convert_data: 根据转轨器配置文件将二进制代码转换为转轨器状态
  - wissel_version: 根据转轨器编号导入配置文件


- HkConfig.ImportIni.py
  - bit_config: 根据配置文件转换转轨器状态， 被convert_data引用
  - byte_config：根据配置文件转换电车数据
  

- ReadAndSave.ImportLog.py
  - read_log: 从log文件中读取数据
  - conver_data: 引用HkConfig类转换数据
  - mapping_df_types: 转换Dataframe数据类型
  - log_to_sql: 将转换后的数据保存到sqlit3数据库
  - set_steps_denbdb3c: 从数据库中读取denbdb3c类型转轨器,匹配状态
  - process_log_sql: 封装转换步骤

- ReadAndSave.VerSelect.py
  - get_version: 输入转轨器编号，返回转轨器类型
  - get_wissel_type_nr: 输入转轨器类型，返回所有该类型转轨器编号
  
- DataBase.ConnectDB.py
  - conn_engine: 连接sqlite3数据库，读取或保存数据库

- Analyze.tram_speed.py
  - wagen_lent: 电车长度数据
  - tram_speed_to_sql: 计算电车速度并保存到数据库

- Run
  - RunText.py: Run程序，针对测试环境封装
  - RunVM.py: Run程序， 针对生成环境封装
  
- Show.Get_data.py
  - get_tram_speed: 从数据库读取电车速度
  - create_download_link: 针对stramlit创建下载链接

- Show.index.py
  - streamlit启动文件，展示stramlit网页

- Show.pages.py
  - stramlit网页配置
