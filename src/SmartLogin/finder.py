# -*- coding: utf-8 -*-
# @Time    : 2017-12-27 17:14
# @Author  : EchoShoot
# @Email   : BiarFordlander@gmail.com
# @URL     : https://github.com/EchoShoot
# @File    : finder.py
# @Explain : 该模块主要功能是,通用性的发现一些元素!方便我们进一步操作!

import logging
from SmartLogin import Errors

__all__ = (
    'smart_get',
    'auto_switch_to_LoginForm',
    'fill_username_and_password',
    'get_username_input',
    'get_password_input',
    'get_frames',
)

logger = logging.getLogger(__name__)


# logger.disabled = True


# 以下是比较成熟的函数
def smart_get(driver, url, timeout=10):
    """ 限制访问的时间,避免等待过长的时间! """
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
    except Errors.TimeoutException:
        driver.set_page_load_timeout(timeout / 3)


def auto_switch_to_LoginForm(driver):
    """ 自动切换到有 LoginForm 的页面,如果没有找到会抛出 LoginFormIsNotFound 异常 """
    if not _is_LoginForm_in_this_page(driver):
        try:
            frames = get_frames(driver)
            logging.info('find {} frames in this page'.format(len(frames)))
            if not _is_LoginForm_in_this_frames(driver, frames):  # 如果这些 frames 中没有 登录表单
                raise Errors.LoginFormIsNotFound("当前页面似乎没有直观可见的登录表单.")
        except Errors.NoSuchElementException:
            raise Errors.LoginFormIsNotFound("当前页面,似乎不是登录页面.")


def fill_username_and_password(driver, username, password):
    try:
        get_username_input(driver).send_keys(username)
        get_password_input(driver).send_keys(password)
    except Errors.ElementNotVisibleException:
        raise Errors.LoginFormIsNotVisible('发现了 LoginForm, 但似乎被遮盖了! 试试在调用本函数前,通过模拟点击,使之显示输入框.'
                                           '例如: driver.find_element_by_xpath("YOUR_XPATH").click()')


# 以下是获取性函数
def get_username_input(driver):
    """ 用来获取用户名输入框 """
    try:
        # # 返回 可见的密码输入框的前驱节点中的所有可见的文本输入框中的第一个!(最靠近密码输入框的那个)
        # # 如果未来再恶劣一点,就获取 pwd 框的宽度,比较
        return driver.find_element_by_xpath(
            '//input[@type="password" and not(contains(@style,"display: none;"))]/preceding::input[not(contains(@style,"display: none;"))][1]')
    except Errors.NoSuchElementException:
        raise Errors.LoginFormIsNotFound('没有找到 username 输入框.')
    except Errors.TimeoutException:
        raise Errors.LoginFormIsNotFound('在有限的时间内,没有找到 username 输入框.')


def get_password_input(driver):
    """ 用来获取密码输入框 """
    try:
        elements = driver.find_elements_by_xpath('//input[@type="password" and not(contains(@style,"display: none;"))]')
        # 如果只有一个就不继续过滤了
        if len(elements) == 1:
            return elements[-1]
        else:
            # 过滤出不反人类的输入框 (输入框通常是长方形,且大小一定会超过9px)
            pwds = [pwd for pwd in elements if 9 < pwd.size['height'] < pwd.size['width']]
            if pwds:
                return pwds[-1]  # 可见的倒数第一个密码框
            else:
                raise Errors.LoginFormIsNotFound('没有找到直观可见的密码输入框.')
    except Errors.NoSuchElementException:
        raise Errors.LoginFormIsNotFound('没有找到 password 输入框.')
    except Errors.TimeoutException:
        raise Errors.LoginFormIsNotFound('在有限的时间内,没有找到 password 输入框.')


def get_frames(driver):
    """ 用来获取所有的 iframe/frame """
    try:
        return driver.find_elements_by_css_selector('iframe,frame')
    except Errors.NoSuchElementException:
        raise Errors.NoSuchElementException('没有找到 iframe or frame.')
    except Errors.TimeoutException:
        raise Errors.NoSuchElementException('在有限的时间内,没有找到 iframe or frame.')


# 以下是判断性函数
def _is_LoginForm_in_this_page(driver):
    """ 用于判断一个页面是否有账号密码框 """
    try:
        get_username_input(driver)
        get_password_input(driver)
    except Errors.LoginFormIsNotFound:
        return False
    else:
        return True


def _is_LoginForm_in_this_frame(driver, frame):
    """ 判断指定的 frame 中是否有 登录表单 """
    driver.switch_to.frame(frame)  # 切换进这个 frame
    if _is_LoginForm_in_this_page(driver):
        return True
    else:
        driver.switch_to.parent_frame()  # 如果没有找到就切换回去
        return False


def _is_LoginForm_in_this_frames(driver, frames):
    """ 判断指定的 frames 中是否有 登录表单 """
    for frame in frames:
        if _is_LoginForm_in_this_frame(driver, frame):
            logging.debug('Founded! We Found LoginFrom in this frame{}'.format(frame))
            return True
        else:
            logging.debug('Not Found LoginFrom in this frame{}'.format(frame))
            continue
    else:
        return False
