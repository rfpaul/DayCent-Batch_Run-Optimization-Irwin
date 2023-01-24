## Delete unneeded directories

##=====================Library imports===============================

import csv
import shutil
import os

##====================Global variables==============================

path_model = "C:\\Illinois_DayCent\\"	#---change this to wherever the model sits---
path_data = path_model+"sites\\FID" #---change this to wherever the data sits---
path_valid = path_model+"fid_loc_landuse_valid.csv" #---this is the list of valid FIDs

sch_dict = {'history':              # Dictionary entry of histories and projections
            ['cornsoyhistory',
             'hayhistory',
             'pasturehistory'],

            'projection':
            ['cornsoyproj',
             'hayproj',
             'pastureproj',
             'miscproj',
             'sgproj']}

##===================Function definitions==========================

def get_hist_set():
# Return a list of tuples in the format (FID, oldhistory)
    hist_set = []
    with open(path_valid, 'r') as valid_csv:
        reader = csv.reader(valid_csv, dialect='excel')
        next(reader, 0)
        for row in reader:
            hist_set.append((int(row[0]), row[3]))
    return hist_set

##=======================================Script Run Block begins================================

delete_these = []
files_to_remove = ['resp.out', 'daily.out', 'soiln.out', 'harvest.csv', 'year_cflows.out']

hist_set = get_hist_set()

for FID, history in hist_set:
    for file in files_to_remove:
        delete_these.append(path_data+"{0}\\aghistory\\{1}".format(str(FID), file))
        delete_these.append(path_data+"{0}\\{1}\\{2}".format(str(FID), history, file))
        for projection in sch_dict['projection']:
            delete_these.append(path_data+"{0}\\{1}2{2}\\{3}".format(str(FID), history, projection, file))

del_counter = 0    

for del_path in delete_these:
    try:
        os.remove(del_path)
        if del_counter == 5000:
            print("Interim progress report. Deleted", del_path)
            del_counter = 0
        del_counter += 1
    except:
        pass