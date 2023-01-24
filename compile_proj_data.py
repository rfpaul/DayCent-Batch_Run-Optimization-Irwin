##==Description===================================

##==Library imports===============================
import sys
import csv
import pandas as pd
import numpy as np
#from datetime import date

##==Global variables==============================
path_model = "C:\\Illinois_DayCent\\"     #---change this to wherever the model sits---
path_data = path_model+"sites\\FID"       #---change this to wherever the data sits---
path_valid = path_model+"fid_loc_landuse_valid.csv" #---this is the list of valid FIDs

year_range = range(2014, 2025) #--These are the years to collect data from

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

# Dictionary associating variables with output file
var_source_dict = dict.fromkeys(['somtc', 'agcacc', 'resp(1)', 'strmac(2)', 'volpac', 'bgcjacc', 'bgcmacc'], '{0}FID_{1}.lis')
var_source_dict.update(dict.fromkeys(['N2Oflux', 'NOflux', 'CH4'], 'year_summary.out'))

# Dictionary associating variable with its useful measure basis
var_val_basis = {'somtc':'delta'}
var_val_basis.update(dict.fromkeys(['agcacc', 'strmac(2)', 'volpac', 'bgcjacc', 'bgcmacc', 'resp(1)'], 'max'))
var_val_basis.update(dict.fromkeys(['N2Oflux', 'NOflux', 'CH4'], 'identity'))

##==Function definitions==========================

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

""" # Deprecated; using pandas data frames makes this obsolete
def make_var_index_dict(file_path):
    index_dict = {}
    with open(file_path, 'r') as file_in:
        line = file_in.readline() # read the line
        line = process_line(line)
        for variable in out_header[1:]:
            try:
                index_dict.update({variable:line.index(variable)})
            except:
                pass
    return index_dict

# Deprecated as above
def process_line(line):
    line = line.strip('\n') # remove endline
    line = line.replace(', ', ',') # remove spaces from vars like strucc(1, 3)
    line = line.split()     # separate into a list
    return line
"""

def start_read(infile, varlist):
# Load the input value into the variable
    df = pd.read_table(infile, sep=r"\s+", index_col=0)
    #df = pd.read_table(infile, sep=r"\s+", index_col=0, parse_dates=True, date_parser=dparse)
    df = df.dropna()
    df = df.loc[year_range.start:year_range.stop, varlist]
    return df

# def dparse (yr): # Deprecated/ unnecessary
#     try:
#         yr_val = float(yr)
#         if (yr_val > 1850 and yr_val < 2100):
#             year = int(yr_val)
#             fraction = yr_val - year
#             day = date.fromordinal(int(fraction*365))
#             this_date = date(year, day.month, day.day)
#             return pd.to_datetime(this_date)
#         else:
#             return pd.NaT
#     except:
#         return pd.NaT

def parse_val(df, year, var):
# Parse the value in the column (dataframe) given based on variable type
    basis = var_val_basis[var]
    if basis == 'delta':
        return delta_val(df, year)
    elif basis == 'max':
        return max_val(df, year)
    else:
        return this_val(df, year)
    

def max_val(df, year):
# The maximum value from year start (non-inclusive) to next year start (inclusive)
    return max(df.loc[year+.001:year+1].dropna())

def delta_val(df, year):
# Delta value associated with this year
    return df.loc[year+1] - df.loc[year]
    

def this_val(df, year):
# Identity: Report first value of the year (does not change)
    return df.loc[year:year+1].dropna().iloc[0]
    

def main(FID):
    history = get_FID_history(FID) # Grab history for this FID
    
#     # Grab sample files to get the column numbers (indices) of variables -- deprecated
#     sample_out_path = path_data+"{0}\\{1}2cornsoyproj\\".format(str(FID), history)+'{0}'
#     var_index = {}
#     for file in set(var_source_dict.values()): # for the file types containing these variables...
#         if file.find('.lis') == -1: # Not a .lis
#             var_index.update(make_var_index_dict(sample_out_path.format(file)))
#         else: # Is a .lis
#             var_index.update(make_var_index_dict(sample_out_path.format(file.format('cornsoyproj', str(FID)))))
    
    for projection in sch_dict['projection']: # Go throught the projections
        filepath = path_data+"{0}\\{1}2{2}\\".format(str(FID), history, projection)
        path_out = filepath+"compiled_{0}-{1}.csv".format(year_range.start, year_range.stop-1)
        
        concat_these = []
        for file in set(var_source_dict.values()):
            # List of variables to grab
            varlist = [key for key, val in var_source_dict.items() if val == file] 
            if file.find('.lis') != -1: # this is the .lis file
                file = file.format(projection, str(FID))
            concat_these.append(start_read(filepath+file, varlist))
        df_collect = pd.concat(concat_these, axis=1) # This is the collection of 
        header = list(df_collect.columns.values)
        df_compile = pd.DataFrame(index=year_range, columns=header)
        df_compile.index.name = 'year'
        for year in year_range:
            for variable in header:
                # Change the appropriate value
                df_compile[variable][year] = parse_val(df_collect[variable], year, variable)
        # Save to CSV
        df_compile.to_csv(path_out)
        

##==Script Run Block begins================================ 

valid_FIDs = get_valid_FIDs()

FID_first = 1    #---Change this to the first FID to start from
FID_last =  1458    #---Change this to the last FID to end at

FIDs = [i for i in valid_FIDs if (i >= FID_first and i <= FID_last)] # Build list from first-to-last FIDs

for FID in FIDs:
    try:
        main(FID)        #---a definition of main() is above---
        if FIDs.index(FID) % 50 == 0:
            print("Interim report: FID{} complete".format(str(FID)))
    except FileNotFoundError:
        print(FID, "failed: Files not found")
        pass
    except KeyboardInterrupt:
        raise
    except:
        print(FID, "failed:",  sys.exc_info()[0])
        pass
    
