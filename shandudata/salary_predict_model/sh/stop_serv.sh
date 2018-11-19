#!/bin/sh

pids=`ps x | grep python | grep salary_predict_serv.py | awk '{print $1}'`
if [ -z "$pids" ] ; then
	echo "no process killed"
else
	kill -9 $pids
	echo "pids "$pids" killed"
fi
