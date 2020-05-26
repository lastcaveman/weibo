#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "cave-weibo",
    version = "0.2.3",
    keywords = ("pip", "weibo","微博","爬虫"),
    description = "weibo base class. 微博 爬虫 基础",
    long_description = "weibo base class. 微博 爬虫 基础",
    license = "MIT Licence",

    url = "https://github.com/lastcaveman/weibo",     
    author = "lastcaveman",
    author_email = "caveman.last@gmail.com",

    py_modules=['weibo'],
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests","datetime"]
)
