##############################################################
#
#  Fitting/forecasting AIRLINE via ARIMA models
#
##############################################################
install.packages("fUnitRoots","tseries","forecast","Box.test")
library(fUnitRoots)
library(tseries)
library(forecast)
library(stats)

data = read.table("D:\\CURSURI\\Advanced Time Series Modelling\\airline.txt",header=TRUE)
head(data)
n = nrow(data)
y = as.double(data[,3])

y=ts(data[,3])
plot(y)


par(mfrow=c(1,3))
plot(y,xlab="month",type="l")
acf(y,lag.max=40)
pacf(y,lag.max=40)

test=1:108
y1 = y[test]
fit1 = Arima(y1,order=c(1,0,0),seasonal=list(order=c(0,0,0),period=12),method="ML")
fit2 = Arima(y1,order=c(1,0,1),seasonal=list(order=c(0,0,0),period=12),method="ML")
fit3 = Arima(y1,order=c(0,1,0),seasonal=list(order=c(0,0,0),period=12),method="ML")
fit3 = Arima(y1,order=c(1,1,1),seasonal=list(order=c(0,0,0),period=12),method="ML")
fit4 = Arima(y1,order=c(1,0,1),seasonal=list(order=c(1,0,0),period=12),method="ML")
fit5 = Arima(y1,order=c(0,1,1),seasonal=list(order=c(1,0,0),period=12),method="ML")
fit6 = Arima(y1,order=c(1,1,0),seasonal=list(order=c(1,0,0),period=12),method="ML")
fit7 = Arima(y1,order=c(1,1,1),seasonal=list(order=c(1,1,1),period=12),method="ML")

aic  = c(fit1$aic,fit2$aic,fit3$aic,fit4$aic,fit5$aic,fit6$aic, fit7$aic)
aicc = c(fit1$aicc,fit2$aicc,fit3$aicc,fit4$aicc,fit5$aicc,fit6$aicc,fit7$aicc )
bic  = c(fit1$bic,fit2$bic,fit3$bic,fit4$bic,fit5$bic,fit6$bic, fit7$bic)
cbind(aic,aicc,bic)

par(mfrow=c(3,7))
ts.plot(y1)
lines(y1+fit1$res,col=2)
acf(fit1$res)
pacf(fit1$res)
ts.plot(y1)
lines(y1+fit2$res,col=2)
acf(fit2$res)
pacf(fit2$res)
ts.plot(y1)
lines(y1+fit3$res,col=2)
acf(fit3$res)
pacf(fit3$res)
ts.plot(y1)
lines(y1+fit4$res,col=2)
acf(fit4$res)
pacf(fit4$res)
ts.plot(y1)
lines(y1+fit5$res,col=2)
acf(fit5$res)
pacf(fit5$res)
ts.plot(y1)
lines(y1+fit6$res,col=2)
acf(fit6$res)
pacf(fit6$res)
ts.plot(y1)
lines(y1+fit7$res,col=2)
acf(fit7$res)
pacf(fit7$res)

# BEST SARIMA MODEL
fit = Arima(y1,order=c(1,1,1),seasonal=list(order=c(1,1,1),period=12),method="ML")
summary(fit)
par(mfrow=c(1,2))
acf(residuals(fit))
pacf(residuals(fit))
Box.test(residuals(fit), lag=10, fitdf=2, type="Ljung")

par(mfrow=c(1,1))
plot(forecast(fit,h=36))
points((n-35):n,y[(n-35):n],col=2,pch=16)
abline(v=108,lty=2)




