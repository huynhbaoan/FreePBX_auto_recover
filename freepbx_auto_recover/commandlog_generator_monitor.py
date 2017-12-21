#!/usr/bin/python
"""Command (bash script) and log generator for GAM command"""

import time
import os
import mmap
import func_email
import bash_executive

log_buffer = bash_executive.bash_execute()
print log_buffer
if log_buffer.find("WARNING:", 0, len(log_buffer)) != -1:
    func_email.email_send_it_monitor_warning(log_buffer)
if log_buffer.find("HTTP session count exceeded", 0, len(log_buffer)) != -1:
    func_email.email_send_it_monitor_down(log_buffer)
