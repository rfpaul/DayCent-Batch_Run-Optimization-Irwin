# REQUIRES RESULTS OF genetic_algorithm.py TO BE PICKLED
# Get a pandas dataframe of each specified individual from
# the Pareto front, and save the landscape to csv
## Module imports
import pickle
import pandas as pd
import numpy as np
from deap import base, creator

## Global variables
# Where are the pickled data objects?
pickPath = "/Users/exnihilo/Dropbox/Rochelle/pickled_data/"
pickPareto = "pareto_2015-07-17 +total +CXuniform +only_cb-h-p popsize=300 weights=(0.5, 0.5, -1.0) NGEN=5000.pkl"
pickdf = "dcent_out_2015-04-29.pkl"

# Register the DEAP base classes
creator.create("Fitness", base.Fitness, weights=(0.5, 0.5, -1.0))
creator.create("Individual", np.ndarray, fitness=creator.Fitness)

# Load objects from pickle files
pickMe = pickPath + pickPareto
hof = pickle.load(open(pickMe, 'rb'))

pickMe = pickPath + pickdf
dcent_out = pd.read_pickle(pickMe)

# Which individuals in the HOF do we want to save to CSV?
TARGETLIST = range(0, len(hof))
# Where are we saving these CSV tables?
savePath = "/Users/exnihilo/Dropbox/Rochelle/pareto_optima_CSVs_without_cellu/pareto_HOF{}.csv"

## Function definition
# Return the projection landscape dataframe from individual
def indivdf(individual):
    # FID list, built from a truncatation of every 5th FID
    fidArray = np.array(dcent_out[::5].index).astype(int)
    # Indices defining our potential solution set
    solveIndex = fidArray + individual
    # Dataframe of our individual solution landscape
    dfSolve = dcent_out.loc[solveIndex]
    # Send back the data frame of our resulting landscape
    return dfSolve
    
## Main function definition
def main():
    for target in TARGETLIST:
        print("Saving table for hof[{}]".format(str(target)))
        df = indivdf(hof[target])
        df.to_csv(savePath.format(str(target)))

## SCRIPT BEGINS
if __name__ == "__main__":
    main()    