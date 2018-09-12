#!/bin/bash


ll=`netstat -tpnl|grep 6886|wc -l`

if [ $ll -eq 1 ];then
echo `ifconfig eth0| grep -oP '(?<=addr:)\S+'`
fi
