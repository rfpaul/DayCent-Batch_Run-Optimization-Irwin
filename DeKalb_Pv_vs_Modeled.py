import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Formatting
mpl.rc_file("/Users/exnihilo/Dropbox/Rochelle/graphs/matplotlibrc")

# Excel file
myData = pd.read_csv(
    "/Users/exnihilo/Dropbox/Rochelle/data/Dekalb_Pv_50kgN_yield.csv",
        header=0)
# Drop extraneous columns
myData.drop(['treatment', 'units', 'mean'], axis=1, inplace=True)

# Data labels, line styles, colors
myData.columns = ['Year', 'measured', 'modeled']
markStyles = ['^', 'o']
pointColors = ['#000000', '#5577DD']

# Plot data
fig = plt.figure(num=111, figsize=[3.150, 3.4])
ax = fig.add_subplot(111)
for label, marker, col in zip(myData.columns[1:], markStyles, pointColors):
    dataPlot = myData.plot(x='Year', y=label, kind='scatter', color=col,
        marker=marker, label=label, ax=ax)
# Legend
dataPlot.legend(ncol = 1, loc=2)
# Y axis label
dataPlot.set_ylabel("Production (g C m$^{-2}$ yr$^{-1}$)")
# X axis formatting
plt.ticklabel_format(style='plain', axis='x', useOffset=False)