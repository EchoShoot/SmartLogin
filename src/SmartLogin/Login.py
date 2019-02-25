# -*- coding: utf-8 -*-
# @Time    : 2019-02-25 09:53
# @Author  : EchoShoot
# @Email   : BiarFordlander@gmail.com
# @URL     : https://github.com/EchoShoot
# @File    : Login.py
# @Explain : 整合登录逻辑

import logging
import shelve
import time
from selenium import webdriver
from SmartLogin import finder
from SmartLogin import monitor
from SmartLogin import Errors

logger = logging.getLogger(__name__)


# logger.disabled = True

class Login(object):
    def __init__(self, login_url, target_page, driver=None):
        self.login_page = login_url  # 登录地址
        self.target_page = target_page  # 目标地址
        self.cookie_db = shelve.open('Cookie', writeback=True)  # 存储Cookie
        self.driver = driver
        if self.driver is None:
            from pkg_resources import resource_filename, Requirement
            driverpath = resource_filename(Requirement.parse('SmartLogin'), 'SmartLogin/resource/chromedriver')
            logger.info("use default chrome driver from path: {}".format(driverpath))
            self.driver = webdriver.Chrome(driverpath)

    def auto_login(self, username, password, click_xpath=None, update=False):
        """ 自动登录到页面, 如果页面存在登录记录, 则跳过登录过程. """
        cookies = self.cookie_db.get(self.login_page, None)  # 提取 cookie
        if update or cookies is None:  # 如果 cookie 不存在
            cookies = self.login(username, password, click_xpath)  # 模拟登录来获取 cookie
            self.cookie_db[self.login_page] = cookies  # 存入 cookie
        else:
            # 一定是先访问网页,才能添加 Cookie 不报错
            self.driver.get(self.target_page)
            self.driver.delete_all_cookies()  # 清空 Cookie 排除干扰
            for cookie in cookies:
                cookie.pop('expiry', None)  # 弹出过期时间,让所有 Cookie 不会过期
                self.driver.add_cookie(cookie)
            self.driver.refresh()  # 刷新使得 Cookie 效果生效
        return cookies

    def login(self, username, password, click_xpath=None):
        """ 自动切换到登录框, 输入账号密码 """
        try:
            finder.smart_get(self.driver, self.login_page, 30)  # 限制跳转到某个网页的加载时间
            finder.auto_switch_to_LoginForm(self.driver)  # 自动切换到有密码输入框的地方
            if click_xpath:  # 有些网页需要点击一下才会切换到密码输入框
                self.driver.find_element_by_xpath(click_xpath).click()
            finder.fill_username_and_password(self.driver, username, password)  # 输入账号密码
            monitor.until_login_page_switch(self.driver)  # 等待页面发生跳转
            cookies = self.driver.get_cookies()  # 获取 Cookie 的操作
        except Errors.NoSuchWindowException as e:
            raise Errors.BrowsersMayClosed("浏览器可能被关闭了.") from e
        else:
            return cookies

    def close(self):
        self.cookie_db.close()
        self.driver.quit()


if __name__ == '__main__':
    login = Login(
        target_page='https://i.qq.com',
        login_url='https://i.qq.com',
    )
    cookie = login.auto_login('username', 'password',
                              click_xpath='//a[@id="switcher_plogin"]',  # 若登录前不需要点击某处可以赋值为None
                              update=True)
    print('拦截到 Cookie: {}'.format(cookie))
    time.sleep(4)  # 延迟4秒便于观察
