# -*- coding: utf-8 -*-
#Copyright (c) 2019 Biar Fordlander
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from setuptools import setup, find_packages

setup(
	name='smartlogin',
	version='0.0.1',
	url='https://github.com/EchoShoot/SmartLogin',
	description='Web General Login Module',
	long_description=open('README.md').read(),
	author='EchoShoot',
	author_email='BiarFordlander@gmail.com',
	license='MIT',
	packages=find_packages('src'),
	package_dir = {'':'src'},
	include_package_data=True,
	zip_safe=False,
	entry_points={
		'console_scripts': ['smartlogin = SmartLogin.command:launch']
	},
	python_requires='>=3.4',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: Chinese (Simplified)',
		"Operating System :: MacOS :: MacOS X",
		'Programming Language :: Python',
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: Implementation :: CPython",
		"Programming Language :: Python :: Implementation :: PyPy",
	],
	install_requires = [
			'selenium>=3.9.0',
	],
)
