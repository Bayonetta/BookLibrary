BookLibrary
===========

一个基于Flask框架的简单图书管理系统


## 搭配环境
 * 输入 sudo apt-get install python-virtualenv 安装virtualenv虚拟机
 * 在项目根目录下执行. venv/bin/activate， 开启虚拟机
 * 输入deactive, 关闭虚拟机
 * 在虚拟机开启情况下，输入python book.py，然后在浏览器中打开127.0.0.1:5000即可访问

 ## 导入数据
 * 进入sqlite3 shell，输入.separator "," 后，再输入 .import books.txt books


