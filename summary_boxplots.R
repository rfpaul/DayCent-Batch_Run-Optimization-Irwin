workpath <- "/Users/exnihilo/Dropbox/Rochelle/"
filename <- "compiled_data_2014-2024.csv"

setwd(workpath)

compiled <- read.csv(filename)

boxplot(compiled$net_ghg~compiled$projection, col='lightgreen', main="Projection Net GHGs", ylab="gCO2 equivalents per sqm")

boxplot(compiled$agcacc~compiled$projection, col='lightgreen', main="Projection Net Above Ground Carbon", ylab="gC per sqm")
