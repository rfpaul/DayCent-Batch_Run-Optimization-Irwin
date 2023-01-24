library(foreach)

filepath <- "/Users/exnihilo/Dropbox/Rochelle/pareto+ssurgo/ssurgo_pareto_HOF30.csv"
result_soil <- read.table(filepath, header=T, sep=',')

projections <- c('cornsoyproj', 'hayproj','miscproj','pastureproj','sgproj')
targetCol <- 'ffd_r'
par(mfrow=c(2,3))

output <- foreach(i=1:length(projections)) %do%
{
	hist(result_soil[,targetCol][result_soil$projection==projections[i]], main=projections[i], xlab=targetCol)
}