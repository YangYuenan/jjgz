# 基金估值查询(jjgz)
## 简介
做本软件的初衷是2023年时主流平台不再提供基金实时估值功能，后来发现基金速查网还能查到实时估值，
之后又学习了一下爬虫相关的技术，便生出了做一个爬取基金估值的软件的想法，今日已经将此想法实现。
此软件仅提供简单的查询基金估值功能，用户可以输入基金代码之后点击添加按钮，程序会自动查询基金代码对应的信息，
并显示在下方表格中，同时会将此基金代码存入配置文件以供之后的查询，除此之外，表格中显示的基金信息可以通过鼠标右键
删除，删除的同时配置文件也会更新。
程序启动后会自动在后台每隔1分钟将所有基金信息更新一遍，并刷新显示。

### 注意
本程序在查询多个基金信息时没有设置延时，使用时请注意不要添加过多的基金代码，以免被封ip，
在测试时曾尝试过单线程无延时连续查询50只基金未被封ip，建议不要超过此值

## 使用的技术
1. 解释器使用python3.10.9
2. gui界面使用Pyqt5实现
3. 爬虫部分使用requests以及xpath实现

## 环境配置
### venv虚拟环境安装配置
```
sudo pip3 install virtualenv
virtualenv venv
. venv/bin/activate
```

### 第三方依赖安装
```
pip3 install -r requirements.txt

```
### 配置文件
1. 配置文件为code.yml，此文件无需修改，通过界面操作时，程序会自动增加或删除配置

## 项目文件说明 
- code.yml  程序配置文件，文件内容为存储的基金代码
- jjgz.py  主界面及程序启动代码
- tableWidget.py  重写的表格控件类
- tools.py  工具函数文件，包括爬虫、配置文件的改写等
- dist  可执行程序目录


本项目目录中的dist文件夹里有打包好的可执行文件（仅限windows）
