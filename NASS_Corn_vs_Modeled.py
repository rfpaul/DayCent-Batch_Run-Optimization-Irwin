import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Formatting
mpl.rc_file("/Users/exnihilo/Dropbox/Rochelle/graphs/matplotlibrc")

# Excel file
myXL = pd.read_excel("/Users/exnihilo/Dropbox/Rochelle/graphs/NASS data, northern IL corn yields.xls", sheetname=1, header=0)
# Drop extraneous columns
myXL.drop(['somtc', 'somsc', 'correlation'], axis=1, inplace=True)


# Data labels, line styles, colors
myXL.columns = ['Year', 'modeled', 'measured']
markStyles = ['o', '^']
pointColors = ['#5577DD', '#000000']

# Only years after 1925
myXL = myXL[myXL.Year > 1925]

# Plot data
fig = plt.figure(num=111, figsize=[3.150, 3.4])
ax = fig.add_subplot(111)
for label, marker, col in zip(myXL.columns[1:], markStyles, pointColors):
    dataPlot = myXL.plot(x='Year', y=label, kind='scatter', color=col,
        marker=marker, label=label, ax=ax)
# Legend
dataPlot.legend(ncol = 1, loc=2)
# Y axis label
dataPlot.set_ylabel("Production (g C m$^{-2}$ yr$^{-1}$)")