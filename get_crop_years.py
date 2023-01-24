# get_crop_years.py
# Compiles a lis with only the data for the years when a specified crop
# is growing. **Requires** a csv referencing the year with the crop grown

# example from the first few lines of cornsoyhistory_crop_schedule.csv:
##    year,crop,schedule,block,year_of_block
##    1847,corn,aghistory,1,1
##    1848,corn,aghistory,1,2
##    1849,corn,aghistory,1,3
##    1850,wheat,aghistory,1,4
##    1851,pasture,aghistory,1,5
##    1852,pasture,aghistory,1,6
##    1853,corn,aghistory,1,1
##    1854,corn,aghistory,1,2


path_model = "C:\\Illinois_DayCent\\"   ## <======= Change this to where the model sits
path_data = path_model+"sites\\FID{0}\\{1}\\{1}FID_{0}.lis"     ## <======= Change this to where the data sits
FID = 859             ## <======= Change this to which FID to pull
use_hist = "cornsoyhistory" ## <====== Change this to the lis to pull
dlim = ',' # <====== Change this to the delimiting character; ',' for CSV, '\t' for LIS
file_ext = ".csv" # <====== Change this to the file type used, ".lis" or ".csv"

lis_source = path_data.format(FID, use_hist) 

crop = "corn" ## <====== Change this to the crop to pull
sched_file = "cornsoyhistory_crop_schedule.csv" ## <========= Change this to the crop schedule summary
path_sched = path_model+sched_file

# Destination of the new .lis; change ...+ ".lis" to ...+ ".csv" if you want a CSV instead
lis_dest = lis_source[:lis_source.find(".lis")] + '_just_' + crop + file_ext

# This keeps track of which years are growing the specified crop type
crop_years = []

with open(path_sched, 'r') as sched:
    # skip header line
    sched.readline()
    for line in sched:
        # get rid of the carriage return
        line = line.rstrip()
        # split into a list by comma delimitation
        line = line.split(',')
        #check that the crop is what we're looking for
        if line[1] == crop:
            #if so, append it onto the list of years where our crop is growing
            crop_years.append(int(line[0]))

with open(lis_source, 'r') as source:
    heading = source.readline()
    heading = heading.split()
    agcprd_status = False
    if heading.index("agcprd") is not -1:
        agcprd_index = heading.index("agcprd")
        heading[agcprd_index] = "agcprd_curr_yr"
        agcprd_status = True

    with open(lis_dest, 'w') as dest:
        dest.write(dlim.join(heading)+'\n')
        heading = source.readline()
        heading = heading.split()

        # Skip the rest of the heading
        while len(heading) < 1:
            heading = source.readline()
            heading = heading.split()
        
        while len(heading[0]) < 4:
            heading = source.readline()
            heading = heading.split()

        last_line = heading
        last_line[0] = '9999'

        for curr_line in source:
            try:
                # split into a list by tab delimitation
                curr_line = curr_line.split()
                # store agcprd's value
                if agcprd_status is True:
                    agcprd_val = curr_line[agcprd_index]
                # determine if the current year is growing our crop
                if int(last_line[0][:4]) in crop_years:
                    # put last year's agcprd value into this year's
                    if agcprd_status is True:
                        last_line[agcprd_index] = agcprd_val
                    # write it into the new .lis file
                    dest.write(dlim.join(str(x) for x in last_line))
                    dest.write('\n')
                last_line = curr_line
            except:
                raise
