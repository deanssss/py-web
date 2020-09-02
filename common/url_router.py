#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from importlib import import_module

def include(module):
    '''根据传入的字符串调用相应的模块。 
    '''
    res = import_module(module)
    urls = getattr(res, 'urls', res)
    return urls

def url_wrapper(urls):
    '''拼接请求url，调用对应的模块。
    '''
    wrapper_list = []
    for url in urls:
        path, handles = url
        if isinstance(handles, (tuple, list)):
            for handle in handles:
                # 分离获取字符串
                pattren, handle_class = handle
                # 拼接url，新的url调用模块
                wrap = ('{0}{1}'.format(path, pattren), handle_class)
                wrapper_list.append(wrap)
        else:
            wrapper_list.append((path, handles))
    return wrapper_list