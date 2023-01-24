# Populate Schedules - populate_schedules.py
# Fills specified FIDs with a new/modified schedule. Inserts the
# appropriate .100 and .wth calls into the .sch files
#

#    Copyright (C) 2012 Robert F Paul, some code (C) 2012 Ira Mabel
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


##=====================Library imports===============================
import os
import csv

##====================Global variables==============================
path_model = "C:\\Illinois_DayCent\\"	#---change this to wherever the model sits---
path_data = path_model+"sites\\FID" #---change this to wherever the data sits---
path_valid = path_model+"fid_loc_landuse_valid.csv" #---this is the list of valid FIDs

schedules = {'history':
             ['aghistory',
              'cornsoyhistory',
              'hayhistory',
              'pasturehistory'
              ],
             
             'projection':
             ['cornsoyproj',
             'hayproj',
             'pastureproj',
             'miscproj',
             'sgproj'
                 ]}  # ---change this to the new schedules to add into the sites---

path_templates = []

for key in schedules:          # build the list of file paths to the schedule templates
    for val in schedules[key]:
        path_templates.append('{0}templates\\{1}.sch'.format(path_model, val))

##===================Function definitions==========================

def get_valid_FIDs():
# Return a list of valid FID values
    valid_list = []
    with open(path_valid, 'r') as valid_csv:
        reader = csv.reader(valid_csv, dialect='excel')
        next(reader, 0)
        for row in reader:
            valid_list.append(int(row[0]))
    return valid_list

def get_FID_history (FID):
# Get the land history asssociated with the FID
    with open(path_valid, 'r') as valid_csv:
        history = csv.reader(valid_csv, dialect='excel')
        found_hist = "INVALID FID"
        next(history, 0)
        for row in history:
            if FID == int(row[0]):  # FID match check
                found_hist = row[3] # The column of land use
                return found_hist
    return found_hist

def index_containing_substring(the_list, substring):
# return the index value of the list element containing substring
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

def write_sch_from_template(FID, sch_source, sch_dest):
# copy template schedule into associated simulation folder within FID
    with open(sch_dest, 'w') as dest:           #opens schedule file for model
        for line in open(sch_source, 'r'):      #opens template file
            if '_.100' in line:                         #changes site file name from template's _.100 placeholder
                dest.write('FID_'+str(FID)+'.100\n')
            elif '_.wth' in line:                       #changes weather file name from template's _.wth placeholder
                dest.write('FID_'+str(FID)+'.wth\n')
            else:                                       #doesn't change any other line
                dest.write(line)
    #print("FID", FID, "has", sch_dest, "added.\n")

##>>>>>>>>>>>>>>>>>>>>>>>>>>>>Main function<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def main(FID):
    history_list = ['aghistory', get_FID_history(FID)]
    
    for history in history_list:
        hist_path = '{0}{1}\\{2}\\'.format(path_data, str(FID), history)  # destination path for .sch file
        temp_path = path_templates[index_containing_substring(path_templates, history)] # path to .sch template
        #print(hist_path, '\n', temp_path, '\n')
        try:
            os.makedirs(hist_path) # write the directory path for the land use history
        except:
            #print("Could not make", hist_path)
            pass
        write_sch_from_template(FID, temp_path, (hist_path + history + '.sch')) # write .sch template to destination

        for projection in schedules['projection']:
            proj_path = '{0}{1}\\{2}2{3}\\'.format(path_data, str(FID), history, projection) # destination path for .sch file
            temp_path = path_templates[index_containing_substring(path_templates, projection)]  # destination path for .sch file
            if history is not 'aghistory':
                try:
                    os.makedirs(proj_path) # write the directory path for projections from history
                except:
                    #print("Could not make", proj_path)
                    pass
                write_sch_from_template(FID, temp_path, (proj_path  + projection + '.sch')) # write .sch template to destination

##=======================================Script Run Block begins================================ 

valid_FIDs = get_valid_FIDs()

FID_first = 1     #---Change this to the first FID to start from
FID_last =  1458    #---Change this to the last FID to end at

FIDs = [i for i in valid_FIDs if (i >= FID_first and i <= FID_last)] # Build list from first-to-last FIDs

for FID in FIDs: # run through and change the proper files
    for index in range(0, len(schedules)):
        main(FID)
    if FID % 100 is 0:
        print("Interim status report: {} completed.".format(FID))

print("Run complete.")
