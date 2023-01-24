#INSTRUCTIONS:
# 1. Put this program in the same folder as DayCent. The field data should also be stored in the same place.
# 2. At the bottom of this file, there are two ways to run DayCent - one for a continuous range of FIDS,
#    one for a selection individual FIDs. Uncomment (delete the #'s) the syntax to use and comment (add #'s) the other
# 3. In the global variables, there's a dictionary named "sch_dict," which defines the histories (which need to be run first
#    from daycent_history.py) and projections to make from each history. Histories and projections can be changed as needed.
#
#   At the conclusion of this program, all files from the DayCent runs will be moved to \sites\FID*\. The messages from each
#   DayCent run are kept as a text file in \output\. DayCent runs that errored will put 'ERROR' at the front of this text file for
#   easy searching

#    Copyright (C) 2012-2014 Ira Mabel, Robert Paul
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
import csv
import os
import shutil
import subprocess

##====================Global variables==============================
path_model = "C:\\Illinois_DayCent\\"     #---change this to wherever the model sits---
path_data = path_model+"sites\\FID"       #---change this to wherever the data sits---
path_valid = path_model+"fid_loc_landuse_valid.csv" #---this is the list of valid FIDs

year_begin = 2012 # This is the beginning date for data
year_end = 2030 # This is the end date for data

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
def get_outfiles():
# Go through outfiles.in and collect output file names into a list
    path_outfiles = path_model+"outfiles.in"
    outfiles = []

    with open(path_outfiles, 'r') as outs:
        for line in outs:
            line = line.split()
            if line[0] is '1':
                outfiles.append(line[1])
    return outfiles

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

def copy_files_in (filenames, path_FID):
#copies files into the DayCent folder for the current field
    for file in filenames:
        try:
            shutil.copy(path_FID+file, path_model)     #---copy command---
            print("Copied file ", file, " into working directory\n")
        except IOError as e:
            print("***ERROR*** Could not find", path_FID+file, '\n')

def DayCent (filename, sch, append):
#runs DayCent for a given field and (schedule_file, output) pair
    #print ("Ready to run ", sch+filename, "\n")
    args = [path_model+'DailyDayCent', '-s', sch, '-n', sch+filename, '-e', append]
        #---all the arguments to run DayCent using thw Windows command line---
    print(" ".join(args))
        #---gets the arguments ready to run the model---
    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
        #---opens the DayCent program---
    results = str(proc.communicate()[0])
        #---runs the DayCent program---
    return save_output(results, 'DayCent_', sch+filename)
        #---saves the output from DayCent to a file

def save_output (results, program, filename):
#saves the DayCent output to a text file
    results = str(results[2:len(results)-1])
        #---strips extra leading and trailing punctuation to make the output readable---
    results = results.replace('\\n','\n')
    results = results.replace('\\r','\r')
    results = results.replace('\\t','\t')
        #---fixes the special characters so the output will write to a file correctly---
    
    if results.find('success') is -1:
        #---if the output does not contain the word 'success', i.e. DayCent ran with errors---
        program = 'ERROR_'+program
            #---add the word "ERROR" to the beginning of the output filename---
        status = False
        print ("***ERROR*** Unsuccessful run of {}\n".format(filename))
    else:
        #---the output from DayCent ran without errors---
        status = True
        print ("Successful run of {}\n".format(filename))
    try:
        os.makedirs(path_model+'output\\')
    except:
        pass
    output = open('{0}output\\{1}{2}.txt'.format(path_model, program, filename), 'w')   #---creates text file---
    output.write(results)           #---saves output to file---
    output.close()
    return status          #---reports whether DayCent ran without errors---

# def get_variables():
#     file_path = path_model+'outvars.txt'
#     with open(file_path, 'r') as outvars:
#         vars = []
#         for line in outvars:
#             line = line.strip()
#             vars.append(line)
#     return vars

# def convert_output (filename, sch):
# #runs DayCent_list100 for FID
#     variables = get_variables()
#     inputs = '{0}\n{0}\n{1}\n{2}\n'.format(sch+filename, '2015', '2029')+'\n'.join(variables)+'\n'      #---inputs for DayCent_list100 program---
#     proc = subprocess.Popen(path_model+'DailyDayCent_list100.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE)    #---runs program---
#     results = str(proc.communicate(inputs.encode())[0])             #---sends inputs, gets output---
#     print("\n\tMade .lis from "+sch+filename+"\n")

def convert_output (filename, sch):
#runs DailyDayCent_list100.exe for FID
    args = [path_model+'DailyDayCent_list100.exe', sch+filename, sch+filename,
            "outvars.txt"] #---inputs for DayCent_list100 program---
        #---all the arguments to run DayCent using thw Windows command line---
    print(" ".join(args))
         #---runs program---
    proc = subprocess.Popen(args,stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        #---sends inputs, gets output---
    results = str(proc.communicate()[0])
    print("\n\tMade .lis from {0}{1}\n".format(sch, filename))


def copy_files_out(files, path_target):
#copies output files to data directory
    try:
        os.mkdir(path_target)   #---makes the target directory if it doesn't exist---
    except OSError:
        pass
    for file in files:
        shutil.copy(path_model+file, path_target)     #---moves files for FID to data directory---
        print("CFO\tCopied {0} to {1}".format(file, path_target))

def clean_up(delete):
#deletes working files
    for file in delete:
        try:
            os.remove(path_model+file)
            print ("CU\tDeleted {0}{1}".format(path_model, file))
        except:
            pass

##>>>>>>>>>>>>>>>>>>>>>>>>>>>>Main function<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def main (FID):
#does all the work for each FID, one at a time
#---definitions for other functions it calls are above---
    filename = 'FID_'+str(FID)              #---creates a convenient string for files associated with FID---
    path_FID = path_data+str(FID)+'\\'      #---the directory for the field data---

    historical = get_FID_history(FID) # Get the historical land use type associated with the FID (from fid_hist_landuse.csv)

    filenames = ['FID_{}.wth'.format(str(FID)),  'FID_{}.100'.format(str(FID)), 'soils.in',
                 '{0}\\{0}FID_{1}.bin'.format(historical, str(FID))]
        #---filenames are the files for each field that DayCent needs to run---
        #---these are the weather file, site file, soils.in, file and any .sch and .bin files required---
    for proj in sch_dict['projection']:
        filenames.append('{0}2{1}\\{1}.sch'.format(historical, proj))
        # These for loops build the list of history .bin and projection .sch files
    
    try:
        copy_files_in(filenames, path_FID)
        #---this copies files defined above into the working directory---
    except:
        pass

    schedules = []
    for proj in sch_dict['projection']:
        schedules.append((proj, historical+filename))
    #---this is the list of schedule files and DayCent output pairs to run---
    #---for example, ('schedule_file', 'output') will work like: 'DayCent -s schedule_file.sch -e output.bin'---
    #---NOTE: THE ORDER IS IMPORTANT! The first pair in the list will run first. If you want to run a pair that---
    #---will be needed by another model run, aghistory for example, make sure that is listed BEFORE the pair that will use it---

    #---list of variables for LIS file. Add or remove as desired---
    
    #output_files = ['nflux.out', 'soiln.out', 'summary.out', 'year_summary.out', 'year_cflows.out', 'harvest.csv']
    #---output files from DayCent, as defined by outfiles.in---
    # *** TARGET FOR REWRITE -- get these directly from  outfiles.in ***

    delete = get_outfiles()
    delete.append('{0}{1}.bin'.format(historical, filename))
        #---list of files to clean from the working directory---

    while (len(schedules) > 0):
    #---this loop will run for each (schedule_file, output) pair listed above
        outputs = get_outfiles()
        #---output files from DayCent, as defined by outfiles.in---

        sch, append = schedules.pop(0)
            #---grabs the first (schedule_file, output) pair in the list---
            #---this is why the order of the schedule files above is important---
        print("Preparing DayCent run of {0} appended to {1}".format(sch, append))
        status = DayCent(filename, sch, append)
            #---runs DayCent for the current field and the (schedule_file, output) pair---
        outputs.append(sch+'.sch')    #---output files from DayCent---
        outputs.append('{0}{1}.bin'.format(sch, filename))
        out_path = '{0}2{1}\\'.format(historical, sch)       #---path to the appropriate history-to-projection folder
        delete.append(sch+'.sch')     #---keeps track of the results to clean up later---
        if status:                                          #---if DayCent ran successfully---
            try:
                convert_output(filename, sch)        #---runs DayCent_list100---
                outputs.append(sch+filename+'.lis')         #---adds the lis file to copy---
                delete.append(sch+filename+'.lis')          #---adds the lis file to delete---
                copy_files_out(outputs, path_FID+out_path)  #---copies output files to data directory\schedule---
                os.remove(path_model+sch+filename+'.bin')   #---delete the new bin after the copy---
            except IOError:
                pass

    delete.extend(['FID_{}.100'.format(str(FID)), 'FID_{}.wth'.format(str(FID)), 'soils.in'])     #---adds the site files to clean up---
    clean_up(delete)    #---deletes the file for the given FID from the working directory---

##=======================================Script Run Block begins================================ 

valid_FIDs = get_valid_FIDs()

FID_first = 1   #---Change this to the first FID to start from
FID_last =  1458   #---Change this to the last FID to end at

FIDs = [i for i in valid_FIDs if (i >= FID_first and i <= FID_last)] # Build list from first-to-last FIDs

for FID in FIDs:
    main(FID)        #---a definition of main() is above---
