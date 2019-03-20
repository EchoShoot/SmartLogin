# SmartLogin
![PyPI](https://img.shields.io/pypi/v/smartlogin.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/smartlogin.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/smartlogin.svg)

Web general login module which based on Selenium

## Feature
- Automatically find the Login-Form.
- Automatically fill in username and password.
- Automatically determine whether the login is successful.
- Support for injecting Jquery for easy execution of JavaScript code.

## Install
```shell
$ pip install smartlogin
```

## Example
```python
from SmartLogin import Login
login = Login.Login(login_url='http://xxx.com', target_page='http://ooo.com')
login.auto_login(username, password, xpath_click='//a[@id="switcher_plogin"]')  
# If you don't need to click button before logging in, you can set `xpath_click` to None.)
```

## Other API
```python
from SmartLogin import finder,monitor
help(finder)  # It can help you find the login form.
help(monitor)  # It can help you listen to page jumps and inject Jquery.
```

## Future Plan
I have noticed Selenium is block widely by E-commerce websites, in next version, i plan to use Puppeteer to improve this API, by that time it may combine with Requests-html which develop by kennethreitz. that would be incomparably convenient, please stay hungry, my friends!