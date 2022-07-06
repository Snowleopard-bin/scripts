#!/bin/bash

while true 
do
	monitor=`ps -ef | grep SV | grep -v grep | wc -l ` 
	if [ $monitor -eq 0 ] 
	then
		echo "SV program is not running, restart SV"
		python3 SV.py
	else
		echo "SV program is running"
	fi
	sleep 5
done