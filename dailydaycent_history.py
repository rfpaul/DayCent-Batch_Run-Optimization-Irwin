#INSTRUCTIONS:
# 1. Put this program in the same folder as DayCent. The field data should also be stored in the same place.
# 2. At the bottom of this file, there are two ways to run DayCent - one for a continuous range of FIDS,
#    one for a selection individual FIDs. Uncomment (delete the #'s) the syntax to use and comment (add #'s) the other
# 3. In the function main(FID) there is a list called 'schedules.' This is a set of schedule file and previous output pairs that
#       DayCent will run. This list can be edited if not all model runs are desired.
# 4.  In the function main(FID) there is a list called 'variables.' These are the variables that will be extracted from the .100 file.
#       This list can be changed to add or remove variables of interest
#
#   At the conclusion of this program, all files from the DayCent runs will be moved to \sites\FID*\. The messages from each
#   DayCent run are kept as a text file in \output\. DayCent runs that errored will put 'ERROR' at the front of this text file for
#   easy searching

#    Copyright (C) 2012-2014 Ira Mabel, Robert Paul
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import os
import shutil
import subprocess
from pathlib import Path


path_model = Path("C:/Illinois_DayCent/")
path_data = path_model / "sites/FID"
path_valid = path_model / "fid_loc_landuse_valid.csv"


def get_outfiles():
    """
    Go through outfiles.in and collect output file names into a list.
    """
    path_outfiles = path_model / "outfiles.in"
    outfiles = []

    with path_outfiles.open('r') as outs:
        for line in outs:
            line = line.split()
            if line[0] == '1':
                outfiles.append(line[1])
    return outfiles


def get_valid_FIDs():
    """
    Return a list of valid FID values.
    """
    valid_list = []
    with path_valid.open('r') as valid_csv:
        reader = csv.reader(valid_csv, dialect='excel')
        next(reader, None)
        for row in reader:
            valid_list.append(int(row[0]))
    return valid_list


def get_FID_history(FID):
    """
    Get the land history associated with the FID.
    """
    with path_valid.open('r') as valid_csv:
        history = csv.reader(valid_csv, dialect='excel')
        found_hist = "INVALID FID"
        next(history, None)
        for row in history:
            if FID == int(row[0]):  # FID match check
                found_hist = row[3]  # The column of land use
                return found_hist
    return found_hist


def copy_files_in(filenames, path_FID):
    """
    Copies files into the DayCent folder for the current field.
    """
    for file in filenames:
        try:
            shutil.copy(path_FID / file, path_model)
            print(f"Copied file {file} into working directory\n")
        except IOError as e:
            print(f"***ERROR*** Could not find {path_FID}{file}\n")


def run_daycent(filename, sch, append):
    """
    Runs DayCent for a given field and (schedule_file, output) pair.
    """
    print(f"Ready to run {sch}{filename}\n")
    args = [str(path_model / "DailyDayCent"), "-s", sch, "-n", f"{sch}{filename}", "-e", append]
    print(" ".join(args))

    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    results = str(proc.communicate()[0])
    return save_output(results, "DayCent_", f"{sch}{filename}")


def save_output(results, program, filename):
    """
    Saves the DayCent output to a text file.
    """
    results = str(results[2:len(results)-1])
    results = results.replace('\\n', '\n')
    results = results.replace('\\r', '\r')
    results = results.replace('\\t', '\t')

    if "success" not in results:
        program = f"ERROR_{program}"
        status = False
        print(f"***ERROR*** Unsuccessful run of {filename}\n")
    else:
        status = True
        print(f"Successful run of {filename}\n")

    output_path = path_model / "output"
    output_path.mkdir(exist_ok=True)

    with (output_path / f"{program}{filename}.txt").open('w') as output:
        output.write(results)
    return status


def convert_output(filename, sch):
    """
    Runs DailyDayCent_list100.exe for FID.
    """
    args = [str(path_model / "DailyDayCent_list100.exe"), f"{sch}{filename}", f"{sch}{filename}", "outvars.txt"]
    print(" ".join(args))

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    results = str(proc.communicate()[0])
    print(f"\n\tMade .lis from {sch}{filename}\n")


def copy_files_out(files, path_target):
    """
    Copies output files to data directory.
    """
    path_target.mkdir(parents=True, exist_ok=True)
    for file in files:
        shutil.copy(path_model / file, path_target)


def clean_up(delete):
    """
    Deletes working files.
    """
    for file in delete:
        try:
            (path_model / file).unlink()
            print(f"X\tDeleting: {file}")
        except OSError:
            pass
    print('\n')


    def main(FID):
        """
        Does all the work for each FID, one at a time.
        """
        filename = f'FID_{FID}'
        path_FID = path_data / str(FID)
        print(f"\nProcessing {filename}...\n")

        # Step 1: Check if FID is valid
        if not get_valid_FIDs(FID):
            print(f"***ERROR*** Invalid FID: {FID}\n")
            return

        # Step 2: Copy files to DayCent folder
        copy_files_in(filenames, path_FID)

        # Step 3: Run DayCent and save output
        results = []
        for sch, append in schedule_files.items():
            success = run_daycent(filename, sch, append)
            results.append(success)

        # Step 4: Convert output files to .lis format
        for sch, _ in schedule_files.items():
            if all(results):  # Check if all runs were successful
                convert_output(filename, sch)

        # Step 5: Copy output files to data directory
        if all(results):
            copy_files_out(files_to_copy_out, path_FID / "output")

        # Step 6: Clean up the working directory
        clean_up(files_to_delete)

        print(f"Done processing {filename}\n")


    if __name__ == "__main__":
        FID = int(input("Enter FID: "))
        main(FID)
