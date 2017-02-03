# coding: utf-8
"""
    multiUA
    ```````
    
    randomizing restccnu User Agent
"""

import os
import random
USER_AGENT_FILE = os.getenv('USER_AGENT_FILE')

def LoadUserAgents(uafile=USER_AGENT_FILE):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip())
    random.shuffle(uas) # 乱序
    return uas
