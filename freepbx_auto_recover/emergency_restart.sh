#!/bin/bash
/usr/bin/pgrep -f asterisk | /usr/bin/xargs kill -15
/usr/local/sbin/fwconsole restart
echo -n > /var/log/asterisk/full
echo "FreePBX executed an emergency restart on $(date)"
echo "Full log is cleared to avoid further warning"
