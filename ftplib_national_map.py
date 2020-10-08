# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 10:21:45 2018

@author: derekolson
"""

###############################################################################
import ftplib
import zipfile
import os
###############################################################################

###############################################################################
## Function to parse through national map
###############################################################################
def list_files():
    files = []
    directories = []
    try:
        #directories = ftp.retrlines('LIST')
        directories = ftp.nlst()
        print(directories)
        for state  in state_list:
            print(state)
            for directory in directories:
                if directory.startswith(state):
                    print(directory)
                    next_dir = '/' + start_here + directory + "/IMG/"
                    print(next_dir)
                    ftp.cwd(next_dir)
                    files = ftp.nlst()
                    print(files)
                    for file in files:
                        ftp.retrbinary('RETR ' + file, open(out_path + file, 'wb').write)             
    except:
        if ftplib.error_perm == "550 No files found":
            print("No files in directory")
        else:
            raise
            
###############################################################################
## Download files 
###############################################################################                
site_address = "rockyftp.cr.usgs.gov"
out_path = 'G:/R8_test/'

with ftplib.FTP(site_address) as ftp:
    ftp.login()  
    print(ftp.getwelcome())
    
    state_list = ['TX', 'OK', 'AR','LA','KY','TN','AL', 'FL', 'GA', 'SC','NC','VA', 'MS'] 

    start_here = "vdelivery/Datasets/Staged/Elevation/1m/Projects/"
    ftp.cwd(start_here)
  
    list_files()
    
###############################################################################
## this test worked for me
#############################################################################
import ftplib

site_address = "rockyftp.cr.usgs.gov"        

out_path = 'G:/R8_test/'
ftp = ftplib.FTP(site_address)
ftp.login()
print(ftp.getwelcome())
state_list = ['TX', 'OK', 'AR','LA','KY','TN','AL', 'FL', 'GA', 'SC','NC','VA', 'MS']

start_here = "vdelivery/Datasets/Staged/Elevation/1m/Projects/"
ftp.cwd(start_here)

dirs = []
files = []
dirs = ftp.nlst()
print(dirs)
for state in state_list:
    print(state)
    for d in dirs:
        if d.startswith(state):
            print(d)
            next_dir = '/' + start_here + d + '/IMG/'
            print(next_dir)
            ftp.cwd(next_dir)
            files = ftp.nlst()
            print(files)
            for file in files:
                ftp.retrbinary('RETR ' + file, open(out_path + file, 'wb').write)