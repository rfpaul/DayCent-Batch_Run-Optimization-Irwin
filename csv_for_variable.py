# csv_for_variable.py
# Create CSV file for the variable

# Iteratively goes through the file structure defined
# to make rows of FIDs, columns of years, and the value of
# the variable defined by FID and year of output.

path_model = "C:\\Illinois_DayCent\\"   ## <======= Change this to where the model sits
path_data = path_model+"sites\\FID"     ## <======= Change this to where the data sits
output_file = 'aghistory'               ## <======= Change this to which output to use
variable = "agcacc"                     ## <======= Change this to which variable to use

start_yr = 1900   ## <======= Change this to starting year
end_yr = 2000     ## <======= Change this to ending year

var_outPath = path_model+output_file+'_'+variable+'.csv'

with open(var_outPath, 'w') as results_setup: ## set the headers
    results_setup.write('FID,')
    for year in range(start_yr, end_yr):
        results_setup.write(str(year)+',')
    results_setup.write(str(end_yr)+'\n')

FIDs = range(1, 1459)

for FID in FIDs:
    output_path = path_data+str(FID)+'\\'+output_file+'\\'
    csv_inPath = output_path+output_file+'FID_'+str(FID)+'.csv'

    print('\nOutput:\t', output_path, '\nCSV in:\t', csv_inPath, '\nCSV out:', var_outPath, '\n')
    try:
        with open(csv_inPath, 'r') as source:
            firstline = source.readline()
            firstline = firstline.strip('\n')
            firstline = firstline.split(',')

            # index position of the variable
            var_index = 1

            source.readline() #skip year 1
            
            with open(var_outPath, 'a') as results:
                for line in source:
                    line = line.strip('\n')
                    line = line.split(',')
                    #print("Going through year", line[0][:4], "at FID" + str(FID))

                    if int(line[0][:4]) in range(start_yr, (end_yr + 1)):
                        #print ("Value for year", line[0][:4], "at FID", FID, "written to CSV")
                        if int(line[0][:4]) == start_yr:
                            #print("Starting year", line[0][:4])
                            results.write(str(FID)+',')
                        if int(line[0][:4]) == end_yr:   
                            results.write(line[var_index]+'\n')
                            #print("Ending year", line[0][:4])
                        else:
                            results.write(line[var_index]+',')
    except:
        pass
