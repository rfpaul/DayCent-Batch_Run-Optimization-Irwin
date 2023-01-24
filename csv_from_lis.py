# csv_from_lis.py
# Create CSV from LIS

# Turns a LIS file into a CSV

# Iteratively goes through the file structure defined
# to turn the specified LIS files into CSVs.

import sys

path_model = "C:\\Illinois_DayCent\\"   ## <======= Change this to where the model sits
path_data = path_model+"sites\\FID"     ## <======= Change this to where the data sits

output_files =  ['aghistory',
                'cornsoyhistory'
                #'hayhistory',
                #'pasturehistory'
                ]               ## <======= Change these to which outputs to use

#FIDs = range(501, 522)
FIDs = [132]

for FID in FIDs:
    for target in output_files:
        output_path = path_data +str(FID) +'\\' +target +'\\'
        
        lisPath = output_path +target +'FID_' +str(FID) +'.lis'
        csvPath = output_path +target +'FID_' +str(FID) +'.csv'   #<==== LIS output
        
##        lisPath = output_path +'year_summary.out'
##        csvPath = output_path +target +'-year_sum-FID_' +str(FID) +'.csv'    #<==== year_summary output

        print('Output:\t{0}\nFile used:\t{1}\nCSV results:\t{2}\n'.format(output_path, lisPath, csvPath))
        try:
            with open(lisPath, 'r') as lis:
                with open(csvPath, 'w') as csv:
                    for line in lis:
                        line = line.strip('\n') # remove endline
                        line = line.replace(', ', ',') # remove spaces from vars like strucc(1, 3)
                        line = line.split()     # separate into a list

##                        if len(line) > 0:       # To handle the annoying whitespace on line 2
##                            if line[0].find('.') != -1:
##                               line[0] = line[0][:line[0].find('.')]# truncate the decimal from year

                        for i in range(0, len(line)):
                            csv.write(line[i])
                            if i < (len(line)-1):   # if it's not the end of the list
                                csv.write(',')      # ...make a comma separation
                            else:
                                csv.write('\n')     # otherwise, newline/new row
        except KeyboardInterrupt:
            sys.exit("Keyboard interruption from user. Quitting.")
        except:
            pass
