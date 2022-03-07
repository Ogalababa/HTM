# 程序简介

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
