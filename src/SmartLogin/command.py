#!/usr/bin/env python3
from SmartLogin import Login
import getpass


def launch():
    login_url = input('"登录页面" URL: ').strip()
    target_page = input('"登录成功后跳转到" URL(若没有请回车): ').strip()
    username = input('请输入 username: ').strip()
    password = getpass.getpass('请输入 password: ')
    xpath_click = input('"用Xpath在登录页面点击何处?" (若没有请回车): ').strip()
    login = Login.Login(login_url, target_page or login_url)
    login.auto_login(username, password, xpath_click)
