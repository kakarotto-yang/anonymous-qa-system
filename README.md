# 匿名问答系统

#### 介绍
一个使用python的Django框架开发的匿名问答系统。作者收到匿名提问会收到邮件提醒，如果提问者设置了邮箱信息，那么也会收到作者的回复提醒，如果没有设置，可以将回复网址复制保存下来查看作者回复。

#### 安装教程

1. 修改message_board/setting.py文件里的MySQL密码为你的密码
2. board/view.py里面需要填写邮箱信息
3. 在终端输入：python manage.py makemigrations
4. 在终端输入：python manage.py migrate
5. 在MySQL中找到board_ifo这个表，添加一条记录，必须保证记录id是1
6. 该系统没有用户注册功能，所以也需要在auth_user这个表添加作者的账号信息
7. 最后终端输入：python manage.py runserver 启动项目
