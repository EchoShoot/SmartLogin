# -*- coding: utf-8 -*-
# @Time    : 2017-12-27 17:14
# @Author  : EchoShoot
# @Email   : BiarFordlander@gmail.com
# @URL     : https://github.com/EchoShoot
# @File    : monitor.py
# @Explain : 该模块主要功能是为了检测一些状态,比如页面是否发生切换?

import uuid
import logging
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from SmartLogin import Errors
from SmartLogin import finder

logger = logging.getLogger(__name__)

__all__ = (
    'execute_with_jquery',
    'until_login_page_switch',
)


# logger.disabled = True


@contextmanager
def execute_with_jquery(driver, jquery_src=None, timeout=10, poll_frequency=1.5):
    """
    用于加载 jquery, 方便我们调用 jquery 来执行命令
    使用方法:
    with execute_with_jquery(self.driver) as jquery:
        jquery.execute_script(jscode)
    """
    if jquery_src is None:
        jquery_src = "https://cdn.bootcss.com/jquery/1.10.2/jquery.min.js"  # Jquery
    jscode = """
            function loadjsfrom(filepath){                                                                                                             
                var fileref=document.createElement('script');  //创建标签 
                fileref.setAttribute("type","text/javascript");  //定义属性type的值为text/javascript 
                fileref.setAttribute("src", filepath);  //文件的地址 
                document.getElementsByTagName("head")[0].appendChild(fileref);
            }
            if (typeof jQuery == 'undefined' || typeof $.attr == 'undefined') {  
                loadjsfrom("%(jquery_src)s");   // 如果没有 jquery 就装载 jquery 后返回 false
                return false
            } else { 
                return true     //如果有 jquery 就返回 true
            }
            """ % {'jquery_src': jquery_src}
    try:
        # 循环检测,直到 jquery 装载完毕!
        WebDriverWait(driver, timeout, poll_frequency).until(
            lambda x: driver.execute_script(jscode)
        )  # 如果返回 true 说明可以使用 jquery 了
        yield driver  # 返回可以执行 jquery 的 driver
    except Errors.TimeoutException as e:
        raise Errors.TimeoutWithJsExecute('你的js脚本执行超时!') from e
    except Errors.WebDriverException as e:
        raise Errors.WrongWithJsExecute('你的js脚本可能有问题!建议你放到浏览器console上执行!\n{}'.format(jscode)) from e


class TokenValid(object):
    """
        TokenValid 原理:
        找到密码输入框,然后调整密码输入框的样式, 该样式是随机生成的就像 token 一样
        不断检测这个 token 有没有消失, 从而判断页面是否发生跳转
    """

    def __init__(self, driver, use_token=True):
        self.driver = driver
        self.init_title = driver.title  # 初始的标题
        self.init_link = driver.current_url  # 初始的链接
        self.__judge_func = None  # 通过 get_valid_judge_func 会自动配置
        self.uuid_token = str(uuid.uuid4())  # 生成 uuid
        self.use_token = use_token

    @classmethod
    def FromRandom(cls, driver):
        """ 预留接口, 暂时无用 """
        return cls(driver)

    @property
    def is_changed(self):
        """ 
            用于判断页面是否发生跳转
            :return: 跳转True / 没跳转False
        """
        if self.__judge_func is None:  # 如果 judge_func 还没有配置
            try:
                if self.use_token is True:
                    self.__config_uuidtoken()  # 配置 bordercode
                else:
                    logger.info('use_token is False, so we choose alternative scheme!')
                    raise Errors.FailToSetTokenValid('用户选择采用备用方案!')
            except Errors.FailToSetTokenValid:
                # 配置失败采用备用方案
                self.__judge_func = self.__title_or_link_is_changed
                logger.info(
                    'we select "{clsname}.__title_or_link_is_changed" as valid function of "{clsname}.is_changed"'.format(
                        clsname=self.__class__.__name__))
            else:
                # 配置成功就采用默认方案
                self.__judge_func = self.__uuidtoken_is_disappear
                logger.info(
                    'we select "{clsname}.__uuidtoken_is_disappear" as valid function of "{clsname}.is_changed"'.format(
                        clsname=self.__class__.__name__))
        return self.__judge_func()  # 返回 judge_func 判断结果

    def __config_uuidtoken(self):
        """ 
            配置 uuidtoken,如果配置失败会抛出 FailToSetTokenValid 异常
        """
        jscode = """var fileref = document.createElement('div');
                    fileref.setAttribute("uuid", '%(uuidtoken)s');
                    document.getElementsByTagName("div")[0].appendChild(fileref);
                 """ % {'uuidtoken': self.uuid_token}
        self.driver.execute_script(jscode)  # 执行这段 js
        try:  # 检测 uuid 是否注入成功
            WebDriverWait(self.driver, 3, 0.5).until_not(
                lambda x: self.__uuidtoken_is_disappear()
            )  # 如果返回 true 说明可以使用 jquery 了
        except Errors.TimeoutException as e:
            raise Errors.FailToSetTokenValid('uuidtoken 配置失败!')

    def __uuidtoken_is_disappear(self):
        """ 用于判断 uuidtoken 是否消失 """
        try:
            self.driver.find_element_by_xpath('//div[@uuid="%(uuidtoken)s"]' % {'uuidtoken': self.uuid_token})
        except Errors.NoSuchElementException as e:
            logging.info('uuidtoken 消失了! 页面发生了跳转!')
            return True
        else:
            return False

    def __title_or_link_is_changed(self):
        """ 标题与URL链接改变的跳转检测 (老式的检测方案了!作为备用方案!) """
        if self.driver.title != self.init_title:
            return True
        elif self.driver.current_url != self.init_link:
            return True
        else:
            return False


class login_page_is_switch(object):
    """
        页面跳转检测逻辑:
        密码输入框对象消失的跳转检测: 对
        TokenValid特征注入的跳转检测: 对
        标题或者URL链接改变的跳转检测: 备用(当 TokenValid 特征不可用时)
    """

    def __init__(self, driver, use_token=True):
        self.driver = driver
        self.tokenvalid = TokenValid(driver, use_token)  # uuidtoken 检测

    def __call__(self, driver):
        pwd = _password_input_is_invisible(driver)  # 判读 pwd 是否为不可见!
        assert isinstance(pwd, bool), "pwd 应该只返回 True or False,不应当有其他可能!"
        # 在 pwd 可见的状态下,进一步通过 uuidtoken 判断页面是否跳转
        return pwd or self.tokenvalid.is_changed


def _password_input_is_invisible(driver):
    """
    判断密码输入框是否消失,如果消失就意味着页面跳转
    :param driver:
    :return:  可见返回False / 不可见返回 True
    """
    try:
        finder.get_password_input(driver)  # 获取 pwd
    except Errors.LoginFormIsNotFound:  # 找不到密码输入框
        return True
    else:
        return False


def until_login_page_switch(driver, use_token=True):
    """
    会在有限的时间内等待直到页面发生跳转!
    20秒,每0.5秒检测一次!直到登录页面发生跳转.
    """
    WebDriverWait(driver, timeout=60, poll_frequency=0.5).until(
        login_page_is_switch(driver, use_token)
    )
