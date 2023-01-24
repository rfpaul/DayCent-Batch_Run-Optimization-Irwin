## PACKAGES

# import array
import pandas as pd
import numpy as np
import datetime as dt
import random
import pickle
# from scoop import futures
from deap import algorithms, base, creator, tools

## GLOBAL VARIABLES
# OS X
filepath, pickFold = ("/Users/exnihilo/Dropbox/Rochelle/",
                      "pickled_data/")

# Windows
#filepath, pickFold = ("C:\\Users\\rpaul\\Dropbox\\Rochelle\\",
#                    "pickled_data\\")

filename = "compiled_data_2014-2024_ONLY-CORN-BEAN.csv"
# !! Is this a new model output file?
newfile = True

# Read CSV into a Pandas data frame
dcent_out = pd.read_csv(filepath+filename)
# Use FID.projection as index (e.g. 42.3)
dcent_out = dcent_out.set_index('FID')
if newfile:
    pickPath = "{0}{1}dcent_out_{2}.pkl".format(filepath,
        pickFold,
        dt.date.today())
    pickle.dump(dcent_out, open(pickPath, 'wb'))

# Create an array with the available FIDs
fidArray = np.array(dcent_out[::5].index).astype(int)

# Create a history + projection grouping object
histProjGroup = dcent_out.groupby(['history', 'projection'])

# List of projection indices
projList = [0.1, #cornbean
            0.3, #hay
            0.5, #pasture
            0.7, #misc
            0.9] #sg

# The dictionary relating the projection indices
# Not currently implemented, here just in case and for reference
projDict = {0.1:'cornsoyproj',
            0.3:'hayproj',
            0.5:'pastureproj',
            0.7:'miscproj',
            0.9:'sgproj'}

## GENETIC ALGORITHM PARAMETERS
# How many complete FIDs do we have?
NUM_SLOTS = len(fidArray)
# How many potential landscapes are we running through the GA per generation?
POPSIZE = 300
# How many generations are we evaluating?
NGEN = 5000
# What is the probability of cross-over?
CXPB = 0.50
# What is the probability of mutation?
MUTPB = 0.15
# We want to MAX corn biomass (weighted 0.5)
# >> Additionally, our MIN floor for corn biomass is CORN_PROD_MIN
# >> This constraint is not reached in the Pareto front
# We want to MAX cellulosic biomass (weighted 0.5)
# We want to MIN net GHGs (CO2 equivalents) (weighted -1.0)
WEIGHTING = (0.5, 0.5, -1.0)
# What are the base values of "business as usual"?
CORN_BASE = histProjGroup['agc_prod'].sum()['cornsoyhistory', 'cornsoyproj']
# CELLU_BASE = histProjGroup['agc_prod'].sum()['hayhistory',
#     'hayproj'] # + histProjGroup['agc_prod'].sum()['pasturehistory',
#     #'pastureproj']
# GHG_BASE = histProjGroup['total_ghg'].sum()['cornsoyhistory',
#     'cornsoyproj'] + histProjGroup['total_ghg'].sum()['hayhistory',
#     'hayproj'] + histProjGroup['total_ghg'].sum()['pasturehistory',
#     'pastureproj']
# A solution cannot remove more than 40% of corn biomass from production!
# This is the amount of corn production expected to be processed
# into ethanol, and intended to be replaced by cellulosic crops.
# Note: Currently there is no risk of a good solution being close
# to this value; it's here only as a sanity check
CORN_PROD_MIN = .6 * CORN_BASE
# 
# # Conceptual individual
# # An individual is a complete landscape with its respective land uses 
# # defined in each FID slot. A population is a collection of potential
# # landscapes. If we were to initialize it without DEAP helpers...
# solutionArray = np.zeros(NUM_SLOTS)
# for i in range(0,NUM_SLOTS):
#     # Randomly fill the array with 0.1, 0.3, 0.5, 0.7, or 0.9
#     # These will be used as projection indexing/lookup values
#     solutionArray[i] = random.choice(projList)
# 
# # Array of indices defining a potential solution landscape
# solveIndex = fidArray + solutionArray
# # Extract the potential solution data frame from the complete model results
# dfSolution = dcent_out.loc[solveIndex]

## DEAP INITIALIZATION & FUNCTION DEFINITIONS
creator.create("Fitness", base.Fitness, weights=WEIGHTING)
creator.create("Individual", np.ndarray, fitness=creator.Fitness)

toolbox = base.Toolbox()
#toolbox.register("map", futures.map)

# Attribute generator--the projection index for FID slot
toolbox.register("proj_index", random.choice, projList)

# Structure initializers--helpers to build individual lanscapes and
# build populations of landscapes
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.proj_index, NUM_SLOTS)
toolbox.register("population", tools.initRepeat, list,
    toolbox.individual)

# Evaluation and GA-associated functions

# Evaluate the projection landscape
def evalLandscape(individual):
    # Indices defining our potential solution set
    solveIndex = fidArray + individual
    # Dataframe of our individual solution landscape
    dfSolve = dcent_out.loc[solveIndex]
    # Corn production in the landscape
    # Let's eventually try doing this per sqm (agcacc) instead of total site production
    # (which is agc_prod=agcacc*sqm and total_ghg=net_ghg*sqm)
    # Would it be more reasonable for land managers to be concerned with
    # per unit area performance or total landscape level performance?
    # Are these different?
    cornProd = dfSolve[dfSolve['projection']=='cornsoyproj']['agc_prod'].sum()
    # Cellulosic crop (hay included) production
    # in the landscape
    celluProd = dfSolve[(dfSolve['projection']=='miscproj') |
        (dfSolve['projection']=='sgproj') |
        (dfSolve['projection']=='hayproj') ]['agc_prod'].sum()
        # Pasture doesn't produce directly exportable cellulose
        #(dfSolve['projection']=='pastureproj')]['agc_prod'].sum()
    # Net GHGs in the landscape
    netGHG = dfSolve['total_ghg'].sum()
    # Send back the evaluated fitness values for our landscape
    return cornProd, celluProd, netGHG

# Function registration of GA evaluate-cross-select methods
# Uniform distribution breaks crox mate, shuffle mutate, NSGA-ii selection
toolbox.register("evaluate", evalLandscape)
toolbox.register("mate", tools.cxUniform, indpb=CXPB)
#toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=MUTPB)
toolbox.register("select", tools.selNSGA2)

## MAIN FUNCTION
def main():
    # Initialize SCOOP parallelization
    #toolbox.register("map", futures.map)
    pop = toolbox.population(n=POPSIZE)
    #hof = tools.HallOfFame(15, similar=np.array_equal)
    # Hall of Fame stores the Pareto front
    hof = tools.ParetoFront(similar=np.array_equal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", min)
    stats.register("max", max)
    # eaSimple genetic algorithm, this is it!
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB,
    #ngen=NGEN, stats=stats, verbose=True)
    #return pop, stats
    ngen=NGEN, stats=stats, halloffame=hof, verbose=True)
    # Now pickle the results so we can have a loadable record of the run
    pickleName = "pareto_{} +restrict-to-corn-bean +total +CXuniform popsize=300 weights={} NGEN={}.pkl".format(str(dt.date.today()),
                                                                      WEIGHTING,
                                                                      NGEN)
    pickPath = filepath+pickFold+pickleName
    pickle.dump(hof, open(pickPath, "wb" ))
    
    return pop, hof, stats

## SCRIPT BEGINS
if __name__ == "__main__":
    # Initialize multiprocessor pool - deprecated into SCOOP
    #pool = Pool()
    #toolbox.register("map", pool.map)
    pop, hof, stats = main()    