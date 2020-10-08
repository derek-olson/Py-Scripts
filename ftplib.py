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
                
                

###############################################################################
## Download files 
###############################################################################                
site_address = "rockyftp.cr.usgs.gov"
with ftplib.FTP(site_address) as ftp:
    ftp.login()  
    print(ftp.getwelcome())
    
    state_list = ['TX', 'OK', 'AR','LA','KY','TN','AL', 'FL', 'GA', 'SC','NC','VA', 'MS'] 

    start_here = "vdelivery/Datasets/Staged/Elevation/1m/Projects/"
    ftp.cwd(start_here)
  
    list_files()
    
###############################################################################     
list_Upload()    
    download = 'USGS_NED_one_meter_x20y340_GA_Georgia_A1_2016_IMG_2018.zip'
    ftp.retrbinary('RETR ' + download, open(download, 'wb').write)
    print('file download sucessful')
    ftp.quit()



savedir = "G:/Region_8/DEMs"
os.chdir(savedir)
###############################################################################
def list_directory():
    try:
          files = []
          files = ftp.retrlines('LIST')
    except:
       if str(ftplib.error_perm) == "550 No files found":
            print("No files in this directory")
       else:
            raise

    for file in files:
        print(file)

 list_directory()        

def list_Download():
try:
      ftp.cwd('directory')
      files = []
      files = ftp.retrlines('LIST')
except:
   if str(ftplib.error_perm) == "550 No files found":
        print("No files in this directory")
   else:
        raise

for file in files:
    print(file)  

def list_Upload():
    try:
          ftp = ftplib.FTP("0.0.0.0")
          ftp.login(username, password)
          ftp.cwd('directory')
          files = []
          files = ftp.retrlines('LIST')
    except:
       if str(ftplib.error_perm) == "550 No files found":
            print("No files in this directory")
       else:
            raise

    for file in files:
        print(file)