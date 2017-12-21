#!/bin/bash
/usr/sbin/asterisk -rx "core restart now"
echo "FreePBX executed an core restart on $(date)"
