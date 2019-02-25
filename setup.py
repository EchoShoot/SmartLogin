from setuptools import setup, find_packages

setup(
	name='SmartLogin',  # 项目名称
	version='1.0.1',  # 项目版本
	url='https://github.com/EchoShoot/SmartLogin',  # 网址
	description='Web General Login Module',  # 简要描述
	author='EchoShoot',  # 作者
	maintainer='BiarFordlander',  # 维护人
	maintainer_email='BiarFordlander@gmail.com',  # 维护人的邮箱
	license='GPL',  # BSD 的自由权太大了,换 GPL 免得人家拿我模块去 "商用"!
	zip_safe=False,  # 有些工具不支持zip压缩，而且压缩后也不方便调试，建议设为 False!
	python_requires='>=3.6',  # 支持的 Py 版本
	packages=find_packages('src'),  # 包含所有src中的包
	package_dir = {'':'src'},  # 告诉distutils包都在src下
	include_package_data=True,
	# 包含 SmartLogin 项目下 resouces 文件夹里面 所有的文件!
	entry_points={
		'console_scripts': ['smartlogin = SmartLogin.command:launch']
	},
	install_requires = [
		'selenium>=3.9.0',
	],  # 模块所依赖的模块包
	classifiers=[
		'Module :: SmartLogin',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GPL License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.6',
	],
)
