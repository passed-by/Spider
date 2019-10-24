# !/usr/bin/python
# -*- coding:utf-8 -*-
# author : liaohuan

from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'u17', '-o', 'novels.json'])