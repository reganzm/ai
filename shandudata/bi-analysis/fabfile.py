# coding: utf-8
from __future__ import unicode_literals

"""
@author: weijinlong
@date: 2017-01-05
"""

from fabx import hosts, env

env.work_on = 'bi-analysis'
env.work_dir = '~/gitlab/bi-analysis'

from fabx.git import pull, test, pre
from fabx.sys import kill, ps, rm, exe
from fabx.server import run_django
from fabx.other import install, install_req
from fabric.api import cd, prefix, run, local
