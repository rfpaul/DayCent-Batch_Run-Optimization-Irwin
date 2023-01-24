"""--- begin header comments ---

list_found_class.py

Print out a list of land uses and their frequencies
among all FIDs based on 2009-2013 CDL (Cropland Data Layer) maps
compiled in fid_cdl_relate.csv

GPL Robert F. Paul 2013-02-14

--- end header comments ---"""


import csv
from collections import Counter

path_model = "C:\\Illinois_DayCent\\"
path_csv = path_model+"fid_cdl_relate.csv"

class_collect = []
look_at = [5, 7, 9, 11, 13] # These are the columns of cropland classifications

with open(path_csv, 'r') as csv_in:
    reader = csv.reader(csv_in, dialect='excel')
    next(reader, 0)
    for row in reader:
        for index in look_at:
            class_collect.append(row[index]) # Collect the class names into a list

class_freqs = Counter(class_collect) # Build a Counter dictionary from the class list

print ("Found the following classifications at frequency:")
for entry in class_freqs.most_common():
    print("\""+entry[0]+"\",", entry[1])    # Print them into a format to make copy-paste from
                                            # the interpreter shell easy