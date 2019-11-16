file<-'/home/phil/work/private/rental/testdata.csv'
dat <- read.csv2(file)
scatter.smooth(dat$orders~dat$time)
plot(dat$time, dat$orders)

data <- data.frame(orders=dat$orders,time=dat$time)
barplot(data)
plot(data)
