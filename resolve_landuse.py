import csv
from collections import Counter

path_model = "C:\\Illinois_DayCent\\"
path_csv = path_model+"fid_cdl_relate.csv"
path_out = path_model+"fid_loc_landuse.csv"

landuse_dict = dict.fromkeys(["Corn", "Sweet Corn", "Soybeans", "Dry Beans"], 'cornsoyhistory')
landuse_dict.update(dict.fromkeys(["Alfalfa", "Pasture/Hay", "Other Hay/Non Alfalfa", "Winter Wheat", "Oats"], 'hayhistory'))
landuse_dict.update(dict.fromkeys(["Grassland Herbaceous", "Grass/Pasture", "Pasture/Grass", "Clover/Wildflowers"], 'pasturehistory'))

look_at = [5, 7, 9, 11, 13] # These are the columns of cropland classifications in fid_cdl_relate.csv

with open(path_csv, 'r') as csv_in:
    with open(path_out, 'w') as csv_out:
        reader = csv.reader(csv_in, dialect='excel')
        writer = csv.writer(csv_out, dialect='excel', lineterminator='\n')
        header = next(reader)
        header = header[0:3]
        header.extend(["landuse", "olduse"])
        writer.writerow(header)
        for row in reader:
            uses = []
            for index in look_at:
                uses.append(landuse_dict.get(row[index], "other"))
            count_use = Counter(uses)
            new_use = count_use.most_common()[0][0]
            if (new_use == 'pasturehistory') or (new_use == 'hayhistory'): # Resolve hay and pasture
                if row[3] == 'pasturehistory':
                    new_use = 'pasturehistory'  # Give preference to old use
                if row[3] == 'hayhistory':
                    new_use = 'hayhistory'      # Give preference to old use
            to_writer = row[0:3]
            to_writer.extend([new_use, row[3]])
            writer.writerow(to_writer)
        