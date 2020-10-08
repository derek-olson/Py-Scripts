# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 13:44:14 2018

@author: derekolson
"""

###############################################################################
import ftplib
import zipfile
import os
###############################################################################



###############################################################################
## get data for Mississippi
#############################################################################

site_address = "www.maris.state.ms.us"

ftp = ftplib.FTP(site_address)
ftp.login()
print(ftp.getwelcome())

start_here = "ftp4DEM/NRCS-SE_2015_DEM_IMG/"
ftp.cwd(start_here)

out_path = '//166.2.126.25/teui1/4_Derek/Region_8_Topographic_Derivatives/MS/DEM/SE/'

dems = []
files = []
dems = ftp.nlst()
print(dems)
for dem in dems:
    print(dem)
    ftp.retrbinary('RETR ' + dem, open(out_path + dem, 'wb').write)
                
                

# ###############################################################################
# ## Download files
# ###############################################################################
# site_address = "rockyftp.cr.usgs.gov"
# with ftplib.FTP(site_address) as ftp:
#     ftp.login()
#     print(ftp.getwelcome())
#
#     state_list = ['TX', 'OK', 'AR','LA','KY','TN','AL', 'FL', 'GA', 'SC','NC','VA', 'MS']
#
#     start_here = "vdelivery/Datasets/Staged/Elevation/1m/Projects/"
#     ftp.cwd(start_here)
#
#     list_files()
#
# ###############################################################################
# list_Upload()
#     download = 'USGS_NED_one_meter_x20y340_GA_Georgia_A1_2016_IMG_2018.zip'
#     ftp.retrbinary('RETR ' + download, open(download, 'wb').write)
#     print('file download sucessful')
#     ftp.quit()
#
#
#
# savedir = "G:/Region_8/DEMs"
# os.chdir(savedir)
# ###############################################################################
# def list_directory():
#     try:
#           files = []
#           files = ftp.retrlines('LIST')
#     except:
#        if str(ftplib.error_perm) == "550 No files found":
#             print("No files in this directory")
#        else:
#             raise
#
#     for file in files:
#         print(file)
#
#  list_directory()
#
# def list_Download():
# try:
#       ftp.cwd('directory')
#       files = []
#       files = ftp.retrlines('LIST')
# except:
#    if str(ftplib.error_perm) == "550 No files found":
#         print("No files in this directory")
#    else:
#         raise
#
# for file in files:
#     print(file)
#
# def list_Upload():
#     try:
#           ftp = ftplib.FTP("0.0.0.0")
#           ftp.login(username, password)
#           ftp.cwd('directory')
#           files = []
#           files = ftp.retrlines('LIST')
#     except:
#        if str(ftplib.error_perm) == "550 No files found":
#             print("No files in this directory")
#        else:
#             raise
#
#     for file in files:
#         print(file)
