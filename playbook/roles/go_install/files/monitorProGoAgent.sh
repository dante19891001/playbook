#!/bin/bash
v_ps_golangServerAgent=`ps -ef|grep golangAgent |grep -v grep|cut -c 9-15`

if [[ ! $v_ps_golangServerAgent ]] || [[ $v_ps_golangServerAgent == "" ]]; then
( nohup /home/deploy/goAgentServer/golangAgent & )
fi 