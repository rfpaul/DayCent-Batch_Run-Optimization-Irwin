# REQUIRES RESULTS OF genetic_algortitm.py TO BE PICKLED
## Module imports
import pickle
import pandas as pd
import numpy as np
from deap import base, creator
## Plotting modules
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

## Global variables
# Where are the pickled data objects?
pickPath = "/Users/exnihilo/Dropbox/Rochelle/pickled_data/"
pickPareto = [
    'pareto_2015-07-17 +total +CXuniform popsize=300 weights=(0.5, 0.5, -1.0) NGEN=5000.pkl',
    'pareto_2015-07-17 +total +CXuniform +only_cb-h-p popsize=300 weights=(0.5, 0.5, -1.0) NGEN=5000.pkl'
    #'pareto_2016-03-02 +restrict-to-corn-bean +total +CXuniform popsize=300 weights=(0.5, 0.5, -1.0) NGEN=5000.pkl'
           ]
# Colors used for each Pareto object (Hex# or name)
paretoColors = ['#4488FF', '#AA0000']
# Labels identifying the Pareto front
labels = ['with cellulosic crops', 'without cellulosic crops']
pickdf = "dcent_out_2015-04-29.pkl"

# Register DEAP base classes
creator.create("Fitness", base.Fitness, weights=(0.5, 0.5, -1.0))
creator.create("Individual", np.ndarray, fitness=creator.Fitness)

# List of Pareto fronts from pickled data
hofs = []

for pareto in pickPareto:
    pickMe = pickPath + pareto
    hofs.append(pickle.load(open(pickMe, 'rb')))

pickMe = pickPath + pickdf
#dcent_out = pickle.load(open(pickMe, 'rb'))
dcent_out = pd.read_pickle(pickMe)

# Are we showing the proportional per sqm values (True)
# or total landscape values (False)?
PROPORTIONAL = False

# Are the ouputs 2D (True) or 3D (False)?
DISP_2D = False

fidArray = np.array(dcent_out[::5].index).astype(int)
cmap=cm.RdYlBu_r

mpl.rc_file("/Users/exnihilo/Dropbox/Rochelle/graphs/matplotlibrc")

## Function definition
# Evaluate the projection landscape
def evalLandscape(individual):
    # Indices defining our potential solution set
    solveIndex = fidArray + individual
    # Dataframe of our individual solution landscape
    dfSolve = dcent_out.loc[solveIndex]
    # Corn production in the landscape
    cornProd = dfSolve[dfSolve['projection']=='cornsoyproj']['agc_prod'].sum()
    # Cellulosic crops (hay included) production
    # in the landscape
    celluProd = dfSolve[(dfSolve['projection']=='miscproj') |
        (dfSolve['projection']=='sgproj') |
        (dfSolve['projection']=='hayproj')]['agc_prod'].sum()
        # (dfSolve['projection']=='pastureproj')]['agc_prod'].sum()
    # Net GHGs in the landscape
    netGHG = dfSolve['total_ghg'].sum()
    if PROPORTIONAL:
        sqmCorn = dfSolve[dfSolve['projection']=='cornsoyproj']['sqm'].sum()
        cornProd = cornProd / sqmCorn
        
        sqmCellu = dfSolve[(dfSolve['projection']=='miscproj') |
            (dfSolve['projection']=='sgproj') |
            (dfSolve['projection']=='hayproj')]['sqm'].sum()
        celluProd = celluProd / sqmCellu
        
        netGHG = netGHG / dfSolve['sqm'].sum()
    # Send back the evaluated fitness values for our landscape
    return cornProd, celluProd, netGHG

def make_3D_graph(x, y, z, zmin):
    # Not yet implemented
    pass

## Script run begins
# Generate 1x1 figure @ position 1, 169 x 91 mm (in inches)
fig = plt.figure(111, figsize=[6.654,3.583])

if DISP_2D:
    ax = fig.add_subplot(111) # 2D
else:
    ax = fig.add_subplot(111, projection='3d') # 3D

# The lists of points along axes
x, y, z = [], [], []

# List of Pareto results
for hof in hofs:
# Capture our individuals from the Pareto front object
    for indiv in hof:
        corn, cellu, ghg = evalLandscape(indiv)
        x.append(corn)
        y.append(cellu)
        z.append(ghg)

# Lists to numpy arrays
xs, ys, zs = np.array(x), np.array(y), np.array(z)

if DISP_2D:
    ax.scatter(xs, ys, c=zs, cmap=cmap, s=markSize) # 2D
else: # 3D
    # Make vertical lines leading up to the point
    # Get the depth of the floor of the 3D plot
    for xi, yi, zi in zip(xs, ys, zs):
        ax.plot([xi, xi],
            [yi, yi],
            [zs.min(), zi],
            # 2pt black 20% transparent dotted lines
            color='black', linestyle=':', alpha=.20, linewidth=2.0) 
    
    # Starting point of the reading frame of xs, ys, zs
    lastIndex = 0
    for hof, thisColor, labelName in zip(hofs, paretoColors, labels):
        # Advance the end of the slice
        endIndex = lastIndex + len(hof)
        ax.scatter3D(xs[lastIndex:endIndex],
            ys[lastIndex:endIndex], 
            zs[lastIndex:endIndex], 
            c=thisColor, depthshade=False, label=labelName)
        # New beginning point for the next slice
        lastIndex = lastIndex + endIndex
    # Plot 2D "shadow" on z floor
    ax.scatter(xs, ys, zs.min().repeat(xs.size), 
        color='black', marker='.', alpha=.20, s=40)
    # Set z limits of bounding box
    ax.set_zlim3d([zs.min(), zs.max()])

# Axis labels
ax.set_xlabel('Corn-bean production (g C yr$^{-1}$)')
ax.set_ylabel('Cellulosic production (g C yr$^{-1}$)')
if not DISP_2D:
    ax.set_zlabel('\n\n\nTotal GHGs (g CO$_2$ equivalent yr$^{-1}$)') # 3D
# Legend
ax.legend(loc=2)

# No title
# if PROPORTIONAL:
#     frameTitle = "Pareto front of crop productivity- and\nGHG sink-optimized landscapes, g C per sqm"
# else:
#     frameTitle = "Pareto front of total crop productivity- and\ntotal GHG sink-optimized landscapes, g C"
# No title
# plt.title(frameTitle)

# cax = fig.add_axes([0.9, 0.2, 0.02, 0.6])
# norm = mpl.colors.Normalize(vmin=min(z), vmax=max(z))
# cb = mpl.colorbar.ColorbarBase(cax,
#     label="Net GHGs (g CO$_2$ equivalent)",
#     cmap=cmap,
#     norm=norm,
#     spacing='proportional')

plt.ion()
plt.tight_layout()
plt.show()
