#!/usr/bin/python
"""Execute lib for bash file"""

import subprocess

def bash_execute():
#    try:
#        output = subprocess.check_output(['./asterisk_health_check.sh'], \
#                 stderr=subprocess.STDOUT)
#    except subprocess.CalledProcessError as err:
#        output = err.output
#   output =(['./.asterisk_health_check.sh'], stdout=PIPE).communicate()[0]
    output = subprocess.Popen(['./asterisk_health_check.sh'], stdout=subprocess.PIPE).communicate()[0]
    return output
