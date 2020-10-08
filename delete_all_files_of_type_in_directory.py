# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:57:53 2018

@author: derekolson
"""

import os

for root, dirs, files in os.walk(r"F:/FireSevDates"):
    for file in files:
        if file.endswith(".zip"):
            os.remove(os.path.join(root, file))