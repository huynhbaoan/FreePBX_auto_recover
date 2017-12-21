#!/bin/bash
date
/usr/sbin/asterisk -rx "sip show peers" | grep "sip peers"
/usr/sbin/asterisk -rx "core show channels" | grep active

total_process=`ps -u asterisk|wc -l|awk '{print $1}'`
echo "Total asterisk process:" $total_process

total_fd=`/usr/sbin/lsof -u asterisk|wc -l|awk '{print $1}'`
echo "Total file descriptors:" $total_fd
if [[ "$total_fd" -gt 10000 ]]
then
        echo "WARNING: Total file descriptors are more than 10000."
fi

total_fd_leaked=`/usr/sbin/lsof -u asterisk|grep -i identify|wc -l|awk '{print $1}'`
echo "Total LEAKED fd:" $total_fd_leaked
if [[ "$total_fd_leaked" -gt 1000 ]]
then
        echo "WARNING: Total LEAKED file descriptors are more than 1000."
        echo "Restart Asterisk core to release leaked connections."
        source core_restart.sh
fi

total_fd_est=`/usr/sbin/lsof -u asterisk|grep EST|wc -l|awk '{print $1}'`
echo "Total ESTABLISH fd:" $total_fd_est
if [[ "$total_fd_est" -gt 5000 ]]
then
        echo "WARNING: Total ESTABLISH file descriptors are more than 5000."
fi

total_http=`netstat -a|grep -i http|wc -l|awk '{print $1}'`
echo "Total HTTP session:" $total_http
if [[ "$total_http" -gt 5000 ]]
then
        echo "WARNING: Total HTTP seesion is more than 5000."
fi

log_warn=`grep "HTTP session count exceeded" /var/log/asterisk/full|tail -n 1`
if [[ -z "$log_warn" ]]
then
	echo "No HTTP seesion warning from log."
else
	echo $log_warn
        source emergency_restart.sh
fi
