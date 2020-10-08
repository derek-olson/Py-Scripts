# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:06:42 2019

@author: derekolson
"""

import json
import csv

with open('//166.2.126.25/teui1/4_Derek/TCA_Website/json/Ochoco_NF_TCA_Data_habitatTypes.csv', 'r') as csv_file:

    reader = csv.DictReader(csv_file, fieldnames = ('ID','PCT_Forest', 'PCT_Range', 'PCT_Shb_Wood', 'PCT_Other'))

    out = json.dumps([row for row in reader], sort_keys=True, indent=4)

    print(out)

    with open('//166.2.126.25/teui1/4_Derek/TCA_Website/json/Ochoco_NF_TCA_Data.json', 'w') as out_file: 
        out_file.write(out)
