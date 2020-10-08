# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:55:59 2019

@author: derekolson
"""

import pandas as pd

bps_data = '//166.2.126.25/teui1/4_Derek/Bridger_Teton_LTA_Mapping/Zonal_Stats/Zonal_Stats_Admin_Bound_2019_05/bps_tabulate_area.csv'

att_data = '//166.2.126.25/teui1/4_Derek/Bridger_Teton_LTA_Mapping/Zonal_Stats/Zonal_Stats_Admin_Bound_2019_05/BT_LTAs_AttTable.csv'

bps = pd.read_csv(bps_data)
att = pd.read_csv(att_data)

bps_field= bps['Z_ID'].tolist()
att_field= att['ID'].tolist()
att_field = [int(i) for i in att_field]

def findUnmatched(list1, list2):
    unmatched = set(list1).difference(set(list2))
    print(list1)
    print(list2)
    print(unmatched)
    return list(unmatched)

findUnmatched(att_field, bps_field)
