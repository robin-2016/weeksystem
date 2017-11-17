![](https://img.shields.io/badge/language-python-blue.svg)![](https://img.shields.io/badge/platform-linux-lightgrey.svg)

##简介

​	周报系统是为团队和小型企业提供周报统计功能的系统。统计内容包括提交时间、提交数量和工作时间，未完成的人员会出现在统计列表中，完成的则不会出现，减轻周报统计的压力。

##周报系统部署

框架：Flask

推荐使用：nginx + uwsgi + supervisor + flask + mysql

###部署步骤：

- nginx的使用不再说明

- mysql版本5.7（已测试）

  创建数据库：

  CREATE DATABASE dbname;

  创建授权用户：

  GRANT ALL PRIVILEGES ON dbname.* to dbname@ip IDENTIFIED BY 'PASSWD';

  创建表和初始数据：

  python manage.py shell

  &gt; &gt; &gt; from manage.py import db

  &gt; &gt; &gt; db.create_all()

  &gt; &gt; &gt; from app.modles import Role,Groups

  &gt; &gt; &gt;Role.insert_role()

   &gt; &gt; &gt;Groups.insert_groups()

  数据库变化使用Flask-migrate迁移框架

  初始化：python manage.py init

  使用迁移脚本：python manage.py db migrate

  更新数据库：python manage.py db upgrade

  之后更新只执行后两步

- 安装pip和Flask依赖

  yum install epel-release

  yum install python-pip

  pip install -r requirements.txt

- 安装uwsgi

  pip install uwsgi

  配置文件config.ini示例

  ```shell
  [uwsgi]
  #uwsgi 启动时所使用的地址与端口
  socket = 127.0.0.1:8001
  #指向网站目录
  chdir = /root/week
  #python 启动程序文件
  wsgi-file = manage.py
  #python 程序内用以启动的application 变量名
  callable = app
  #处理器数
  processes = 4
  #线程数
  threads = 2
  #状态检测地址
  stats = 127.0.0.1:9191
  ```

- 安装supervisor

  yum install supervisor

  配置文件示例：

  ```shell
  [program:week]
  # 启动命令入口
  command=/usr/bin/uwsgi /root/config.ini
  # 命令程序所在目录
  directory=/root/week
  #运行命令的用户名
  user=root        
  autostart=true
  autorestart=true
  #日志地址
  stdout_logfile=/data/logs/uwsgi_supervisor.log
  ```

- 升级为管理员账号

  注册用户，更改users表role_id为1即为管理员账号，可以进行组管理和角色管理

  角色分为：admin\renli\user