# coding: utf-8

"""
@author: weijinlong
@date: 2017-01-05
"""

from fabx import hosts, env

env.work_on = 'sxz'
env.work_dir = '~/gitlab/salary_predict_model'

from fabx.git import pull, test, pre
from fabx.sys import kill, ps, rm, exe
from fabx.server import run_django
from fabx.other import install
from fabric.api import cd, prefix, run, local


def deploy(service="start", remote="true"):
    """发布 BI web 项目"""
    if service not in ['start', 'restart', 'stop']:
        return
    if service == "restart":
        cmd = "uwsgi --reload /home/bigdata/gitlab/salary_predict_model/uwsgi_sxz.pid"
    elif service == "stop":
        cmd = "uwsgi --stop /home/bigdata/gitlab/salary_predict_model/uwsgi_sxz.pid"
    else:
        cmd = "uwsgi --ini /home/bigdata/gitlab/salary_predict_model/deploy/uwsgi/uwsgi_sxz.ini"

    if remote.lower() == 'true':
        with cd(env.work_dir), prefix(env.virtualenv_workon_prefix % env.work_on), prefix(env.python_path):
            run(cmd)
    else:
        local(cmd)
