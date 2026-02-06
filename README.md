BookLibrary
===========

一个基于 Flask 的简单教学用图书管理系统（已更新到 Python 3）。

功能包括：
- 读者注册 / 登录
- 图书查询、查看详情
- 借书（同一用户最多 3 本）
- 借阅历史查询
- 简单的图书预约（图书已被借出时可预约）
- 管理员登录，进行图书和用户管理

## 环境准备（推荐）

在项目根目录下执行：

```bash
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
pip install flask werkzeug
```

需要安装 sqlite3（大多数系统已自带，如无可使用包管理器安装）。

## 初始化数据库

在项目根目录执行：

```bash
sqlite3 book.db < book.sql
```

## 导入示例图书数据

在项目根目录执行：

```bash
sqlite3 book.db
.separator ","
.import books.txt books
.quit
```

## 运行项目

在虚拟环境激活的情况下，在项目根目录执行：

```bash
python book.py
```

然后在浏览器中打开：

```text
http://127.0.0.1:5000/
```

即可访问系统。
