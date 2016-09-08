# coding: utf-8
"""
    multiUA
    ```````
    
    randomizing restccnu User Agent
"""

import os
import random
USER_AGENT_FILE = os.getenv('USER_AGENT_FILE') or \
                  "/root/www/restccnu/fuckccnu/multiUA/user_agents.txt"


def LoadUserAgents(uafile=USER_AGENT_FILE):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas
