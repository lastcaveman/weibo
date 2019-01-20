#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "cave-weibo",
    version = "0.1.7",
    keywords = ("pip", "weibo","微博","爬虫"),
    description = "weibo base class. 微博 爬虫 基础",
    long_description = "Aweibo base class. 微博 爬虫 基础",
    license = "MIT Licence",

    url = "https://github.com/lastcaveman/weibo",     
    author = "lastcaveman",
    author_email = "caveman.last@gmail.com",

    py_modules=['weibo'],
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests","configparser"]          #这个项目需要的第三方库
)