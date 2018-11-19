# -*- coding: utf-8 -*-
"""
:Author  : weijinlong
:Time    : 22/07/2018 11:32
:File    : __init__.py.py
"""


from .settings import *

try:
    from settings.settings_dev import *
    print('调试在config/settings/添加settings_dev.py文件')
except ImportError as e:
    print('!!!特别注意: 这是在生产环境配置文件下.')
