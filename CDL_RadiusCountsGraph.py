import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.ion()
fig, ax = plt.subplots()
cdlCount = pd.read_csv("/Users/exnihilo/Box Sync/GIS/Rochelle/CDL2012-radius_pixel_counts.txt")
cdlCount.sort(columns='Count', ascending=False, inplace=True)

cdlSlice = cdlCount[cdlCount.Count > 50000]

# Bar graph
# 1 pixel = 0.09 ha
ax.bar(left=np.arange(len(cdlSlice)), height=cdlSlice.Count*0.09, align='center')
plt.xticks(np.arange(len(cdlSlice)), rotation=45, fontsize=10, ha='right')
ax.set_xticklabels(list(cdlSlice.Class_Name))

plt.title("CDL classifications in 70km radius fuelshed for 2012")
plt.ylabel("Area (ha)")

plt.show()