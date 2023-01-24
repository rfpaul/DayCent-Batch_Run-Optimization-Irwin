## Package imports
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

## Global variables
# Formatting
mpl.rc_file("/Users/exnihilo/Dropbox/Rochelle/graphs/matplotlibrc")

## Script run begins
# Get the data
summary = pd.read_csv(
    "/Users/exnihilo/Dropbox/Rochelle/compiled_data_2014-2024.csv")

# Colors and labels   
projections = ['cornsoyproj', 'hayproj', 'pastureproj', 'miscproj', 'sgproj']
projLabels = ['Corn-bean', 'Hay', 'Pasture',
    'Miscanthus x giganteus', 'P. virgatum']
colors = ['darkgoldenrod', 'orange', 'darkred', 'lightgreen', 'lightblue']

# Generate 1x2 figure @ position 1, 169 x 91 mm (in inches)
fig = plt.figure(121, figsize=[6.654,3.583])
# Panel 1, 1
ax1 = fig.add_subplot(121)
# Panel 1, 2
ax2 = fig.add_subplot(122)

# Productivity
prodData = []
# GHGs
ghgData = []
# Fill data in the lists
for proj in projections:
    prodData.append(summary[summary['projection']==proj]['agcacc'])
    ghgData.append(summary[summary['projection']==proj]['net_ghg'])

# Boxplots of list data
bp1 = ax1.boxplot(prodData, patch_artist = True)
bp2 = ax2.boxplot(ghgData,  patch_artist = True)

# Set line widths, colors, etc.
for bplot in [bp1, bp2]:
    for i, box in enumerate(bplot['boxes']):
        box.set(linewidth = .7)
        box.set_facecolor('lightgray')
    for whisker in bplot['whiskers']:
        whisker.set(linewidth=1.5, linestyle=':')
    for cap in bplot['caps']:
        cap.set(linewidth=0.7)
    for flier in bplot['fliers']:
        flier.set(marker='.', color='black', markersize=5, alpha=0.3)

# Y axis labels
ax1.set_ylabel('Production (g C m$^{-2}$ yr$^{-1}$)')
ax2.set_ylabel('Net GHGs (g CO$_2$ equivalent m$^{-2}$ yr$^{-1}$)')

# X tick labels, non-italic
ax1.set_xticklabels(projLabels[0:3], rotation=30, ha='right')
ax2.set_xticklabels(projLabels[0:3], rotation=30, ha='right')

# Subplot labels
ax1.text(-1.0, 2000, '(a)', size=16, fontweight='bold')
ax2.text(-1.0, 500, '(b)', size=16, fontweight='bold')

# X tick labels, italic text
ax1.text(4, -120, projLabels[3], fontstyle='italic',
    rotation=30, ha='right')
ax1.text(5, -120, projLabels[4], fontstyle='italic',
    rotation=30, ha='right')

ax2.text(4, -2150, projLabels[3], fontstyle='italic',
    rotation=30, ha='right')
ax2.text(5, -2150, projLabels[4], fontstyle='italic',
    rotation=30, ha='right')