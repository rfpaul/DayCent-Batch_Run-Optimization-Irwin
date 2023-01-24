#import functions
import os
import math
from datetime import date

dmet_path = "C:\\daymet\\results\\wth_FID{}.csv"
dcent_path = "C:\\Illinois_DayCent\\sites\\FID{0}\\FID_{0}.wth"
##wind_path = "C:\\daymet\\NCDC_DeKalb_Muni_Station.csv"

##dmet_path = "/Users/exnihilo/csv/results/wth_FID{}.csv"
##dcent_path = "/Users/exnihilo/csv/wth/FID{0}/FID_{0}.wth"
##wind_path = "/Users/exnihilo/csv/NCDC_DeKalb_Muni_Station.csv"

# str2num: take a string; return an integer or floating point value
def str2num (string):
    try:
        return int(string)
    except:
        return float(string)

# Get the NCDC wind speed data into a dictionary, referenced by date as key
##def makeDict():
##    wspd_dict = {}
##    try:
##        with open(wind_path, 'r') as wspd:
##            for line in wspd:
##                line = line.rstrip()
##                line = line.split(',')
##                line[1] = float(line[1])
##                this_day = date(1, int(line[0][4:6]), int(line[0][6:]))
##                wspd_dict.update({this_day:line[1]})
##    except:
##        raise
##    return wspd_dict

# Returns a number as a string to the thousandth place
def two_figs(value):
    return ('%.2f' % value)

# Take the DayMet values and convert to a line for DayCent weather file
def makeDayCentEntry(dmet):
    dcent = [-99.9, -99.9, -99.9, -99.9, -99.9,
             -99.9, -99.9]
    # Get the date and record the day
    the_day = date.fromordinal(dmet[1])
    dcent[0] = the_day.day
    # Record the month
    dcent[1] = the_day.month
    # Get year
    dcent[2] = dmet[0]
    # Get day of year
    dcent[3] = dmet[1]
    # Get max temp *C
    dcent[4] = two_figs(dmet[2])
    # Get min temp *C
    dcent[5] = two_figs(dmet[3])
    # Convert mm precip to cm
    dcent[6] = two_figs(dmet[5]/10)
    #The following functions are for extra weather drivers--not to be used yet
##    # Convert Wm^-2 to Langleys/day
##    dcent[7] = two_figs(round((dmet[6]/2.06363), 2))
##    # Convert vapor pressure (in Pa) to relative humidity %
##    svp = 610.78 * math.exp(dmet[2] / (dmet[2]+238.3) * 17.2694)
##    dcent[8] = two_figs(round((100*(dmet[8] / svp)), 2))
##    dcent[9] = two_figs(wspd_dict[the_day])

    return dcent

for FID in range(359, 1459):        
    try:
    # Rename old weather file as FID_(current).wth_old
        os.rename(dcent_path.format(FID), dcent_path.format(FID)+'_old01')

        header_skipped = False

        # Write a new .wth file at current FID
        with open(dcent_path.format(FID), 'w') as wth:
            # Open DayMet CSV at current FID
            with open(dmet_path.format(FID), 'r') as csv:
                for dmet in csv:

                    # Skip first seven lines of DayMet CSV file
                    if not header_skipped:
                        for x in range(0,7):
                            dmet = csv.readline()
                        header_skipped = True
                        
                    # Take line, split by commas, remove \n character
                    dmet = dmet.rstrip()
                    dmet = dmet.split(',')

                    # Convert string values to ints or floats

                    for i in range(0, len(dmet)):
                        dmet[i] = str2num(dmet[i])

                    # Fill list of DayCent line from DayMet values
                    dcent = makeDayCentEntry(dmet)

                    # Concatenate with \t character between DayCent values
                    # and \n at the end into FID_(current).wth
                    wth.write('\t'.join(str(x) for x in dcent))
                    wth.write('\n')
        print ("DayMet => DayCent conversion for FID{} complete.".format(FID))
    except:
        pass
