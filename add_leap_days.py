import fileinput
import sys

wth_path = "C:\\Illinois_DayCent\\sites\\FID{0}\\FID_{0}.wth"
#new_path = "C:\\Illinois_DayCent\\sites\\FID{0}\\FID_{0}.new"

# Turns the line into a list; converts year and day of year to ints
def procLine(line):
    line = line.rstrip()
    line = line.split('\t')
    line[2] = int(line[2])
    line[3] = int(line[3])
    return line

for FID in range(2, 1459):
    leaping = False
    try:
        for line in fileinput.input(wth_path.format(FID), inplace=1):
##        with open(wth_path.format(FID), 'r') as source:
##            with open(new_path.format(FID), 'w') as new:
##                for line in source:
            line = procLine(line)
            if (line[2] % 4 == 0):
                if (line[3] == 59):
                    leaping = True
                    sys.stdout.write('\t'.join(str(x) for x in line)+'\n')
                    line[0] = 29
            else:
                leaping = False
            if(leaping):
                line[3] += 1
            sys.stdout.write('\t'.join(str(x) for x in line)+'\n')
        fileinput.close()
        print("FID_{}.wth was processed to add leap days".format(FID))
    except:
        #raise
        print("FID_{}.wth failed".format(FID))
