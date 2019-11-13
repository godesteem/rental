file<-'/home/phil/work/private/rental/testdata.csv'
dat <- read.csv2(file)
scatter.smooth(dat$orders, dat$time)
