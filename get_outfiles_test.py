path_model = "C:\\Illinois_DayCent\\"
path_outfiles = path_model+"outfiles.in"
outfiles = []

with open(path_outfiles, 'r') as outs:
    for line in outs:
        line = line.split()
        if line[0] is '1':
            outfiles.append(line[1])
