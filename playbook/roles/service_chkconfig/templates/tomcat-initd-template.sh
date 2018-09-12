#!/bin/bash
#
# chkconfig: 345 58 59
# description: Starts/Stops Apache Tomcat
. /etc/rc.d/init.d/functions
export JAVA_HOME="/usr/java/jdk1.7.0_79"

TOMCAT_USAGE="Usage: $0 {\e[00;32mstart\e[00m|\e[00;31mstop\e[00m|\e[00;32mstatus\e[00m|\e[00;31mrestart\e[00m}"

tomcat_path=({% for host in CATALINA_HOME %} {{ host }} {% endfor %})

. /etc/rc.d/init.d/tomcat
