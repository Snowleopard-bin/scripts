# 安装
1. 安装python3环境
2. 安装sqlite3
官网下载源码：https://www.sqlite.org/download.html
```bash
tar -xzvf sqlite-autoconf-3370000.tar.gz
cd sqlite-autoconf-3370000
./configure
make
sudo make install
cd ..
```

安装python sqlite3接口
```bash
pip3 install pysqlite3
```

3. 安装lxml
```bash
pip3 install lxml
```
# 配置文件
配置文件 config.ini 放置在与程序同一个文件夹下，用于设置待提取数据所在的根目录以及保存的数据库名称

# python脚本说明
run.py 为主运行脚本，读取配置文件参数，负责主逻辑
parse.py 解析 html 文件提取数据
get_dir_files.py 用于遍历目录，寻找目标 html 文件
db.py 负责面向数据库的操作
myutils.py 包含部分通用功能

