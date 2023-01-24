import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.ion()
fig, ax = plt.subplots()
soilData = pd.read_excel("/Users/exnihilo/Dropbox/Rochelle/data/final_soils_w_landuse.xlsx")
landGroup = soilData.groupby(by='Land use')

# Sum of areas by 
print(landGroup.sum())

soilData.boxplot(column='hectares', by='Land use')

plt.title("Areas of parcels by land use")
plt.ylabel("Area (ha)")

plt.show()