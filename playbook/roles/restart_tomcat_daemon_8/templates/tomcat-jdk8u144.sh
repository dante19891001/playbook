#!/bin/bash
# chkconfig: 2345 60 80
# description: script for tomcat start

CATALINA_HOMES=({% for host in CATALINA_HOME %} {{ host }} {% endfor %})
TOMCAT_USER=tomcat
JAVA_HOME=/usr/java/jdk1.8.0_144

function jsvc_exec() {
    retval=0
    for CATALINA_HOME in ${CATALINA_HOMES[@]}
    do
        [ $retval -eq 0 ] || [ $retval -eq 255 ] || break
        ${CATALINA_HOME}/bin/daemon.sh \
            --java-home $JAVA_HOME \
            --catalina-home $CATALINA_HOME \
            --catalina-base $CATALINA_HOME \
            --tomcat-user $TOMCAT_USER \
            --service-start-wait-time 50 \
            $1
        retval=$?
    done
    return $retval
}

case "$1" in
    start   )
      jsvc_exec start
      exit $?
    ;;
    stop    )
      jsvc_exec stop
      exit $?
    ;;
    restart  )
      jsvc_exec stop
      sleep 1
      jsvc_exec start
      exit $?
    ;;
    version    )
      jsvc_exec version
      exit $?
    ;;
    *       )
      echo "Unknown command: \`$1'"
      echo "commands:"
      echo "  restart           Retart Tomcat"
      echo "  start             Start Tomcat"
      echo "  stop              Stop Tomcat"
      echo "  version           What version of commons daemon and Tomcat"
      echo "                    are you running?"
      exit 1
    ;;
esac