# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 19:17:02 2021

@author: Arric Hamilton
"""

import subprocess
import os

#kill PID
subprocess = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
output, error = subprocess.communicate()

target_process = "fbcp"
for line in output.splitlines():
    if target_process in str(line):
        pid = int(line.split(None, 1)[0])
        os.kill(pid, 9)
        
#reopen PID
subprocess.Popen([r'fbcp'])