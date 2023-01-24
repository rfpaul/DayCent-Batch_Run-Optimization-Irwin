##==Description===================================

##==Library imports===============================
import sys
import csv
import pandas as pd
import numpy as np

##==Global variables==============================
path_model = "C:\\Illinois_DayCent\\"     #---change this to wherever the model sits---
path_data = path_model+"sites\\FID"       #---change this to wherever the data sits---
path_valid = path_model+"fid_loc_landuse_valid.csv" #---this is the list of valid FIDs

year_range = range(2014, 2025) #--These are the years to collect data from

out_path = path_model+"means_{0}-{1}.csv".format(year_range.start, year_range.stop-1)

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

sub_index_dict = {  'cornsoyproj':  0.1,
                    'hayproj':      0.3,
                    'pastureproj':  0.5,
                    'miscproj':     0.7,
                    'sgproj':       0.9
                  }

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

def start_read(infile):
# Load the input value into the variable
    df = pd.read_csv(infile, index_col=0)
    #df = pd.read_table(infile, sep=r"\s+", index_col=0, parse_dates=True, date_parser=dparse)
    df = df.dropna()
    return df

def process_means(data_series, FID, proj):
    line_dict = data_series.to_dict()
    line_dict.update({'FID':sub_index_dict[proj]+FID})
    line_dict.update({'projection':proj})
    return line_dict

def write_output(data):
# Write the results to output file
    # Make a dataframe from the list of dicts
    final_df = pd.DataFrame.from_dict(data)
    # Define FID column as the index
    final_df.set_index('FID', inplace=True)
    # Get column names
    col_list = final_df.columns.tolist()
    # Rearrange the projection column to be first in the list
    col_list.insert(0, col_list.pop(col_list.index('projection')))
    # Rearrange the dataframe columns
    final_df = final_df[col_list]
    
    final_df.to_csv(out_path)

def main (FID):
    history = get_FID_history(FID) # Grab history for this FID
    data = []
        
    for projection in sch_dict['projection']: # Go throught the projections
        filepath = path_data+"{0}\\{1}2{2}\\".format(str(FID), history, projection)
        path_in = filepath+"compiled_{0}-{1}.csv".format(year_range.start, year_range.stop-1)
        
        df_in = start_read(path_in)
        
        means = df_in.mean()
        
        data.append(process_means(means, FID, projection))
        
    return data

##==Script Run Block begins================================ 

data_list = []

valid_FIDs = get_valid_FIDs()

FID_first = 1    #---Change this to the first FID to start from
FID_last =  1458    #---Change this to the last FID to end at

FIDs = [i for i in valid_FIDs if (i >= FID_first and i <= FID_last)] # Build list from first-to-last FIDs

for FID in FIDs:
    try:
        data_list.extend(main(FID))       #---a definition of main() is above---
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

write_output(data_list)