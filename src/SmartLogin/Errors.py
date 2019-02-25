# -*- coding: utf-8 -*-
# @Time    : 2017-12-28 12:59
# @Author  : EchoShoot
# @Email   : BiarFordlander@gmail.com
# @URL     : https://github.com/EchoShoot
# @File    : Errors.py
# @Explain : 该模块主要功能是各种错误定义

# from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.common.exceptions import *


class BrowsersMayClosed(NoSuchWindowException):
    """ 发现浏览器可能被已关闭 """


class LoginFormIsNotFound(NoSuchElementException):
    """ 没有发现账号密码输入框 """


class LoginFormIsNotVisible(NoSuchElementException):
    """ 发现的账号密码输入框,但是不可见! """


class WrongWithJsExecute(WebDriverException):
    """ 在执行 js 的时候发生了一些错误 """


class TimeoutWithJsExecute(TimeoutException):
    """ 等待 js 执行发生了超时 """


class FailToSetTokenValid(WrongWithJsExecute):
    """ 执行 js TokenValid 注入失败 """


class TargetEmergence(Exception):
    """ 当等待的目标出现的时候抛出 """
