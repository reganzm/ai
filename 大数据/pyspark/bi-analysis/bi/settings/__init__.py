# -*- coding: utf-8 -*-
"""
@author: weijinlong
@Date: 2018-04-11
@Content: 
"""
from __future__ import absolute_import, unicode_literals

from bi.settings.settings import *

try:
    from bi.settings.settings_dev import *
except ImportError as ie:
    print("Production Environment!!!")
except ModuleNotFoundError as mnfe:
    pass
