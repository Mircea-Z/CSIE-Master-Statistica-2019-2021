##############################################################
#
#  Fitting/forecasting GDP (PIB) via ARIMA models
#
##############################################################
install.packages("fUnitRoots","tseries","forecast","Box.test")
library(fUnitRoots)
library(tseries)
library(forecast)
library(stats)

macro = read.csv("D:\\CURSURI\\Advanced Time Series Modelling\\macro.csv",header=TRUE)

attach(macro)

n = nrow(macro)

dPIB = diff(PIB)

year = 1996:2014
ind = seq(1,nrow(macro),by=12)

par(mfrow=c(2,3))
plot(PIB,xlab="Ano",axes=FALSE,type="l")
axis(2);box();axis(1,at=ind,lab=year)
acf(PIB)
pacf(PIB)
plot(dPIB,xlab="Ano",axes=FALSE,type="l")
axis(2);box();axis(1,at=ind,lab=year)
acf(dPIB)
pacf(dPIB)

###############################
# Escolhando a ordem do ARIMA
###############################
aics = NULL
bics = NULL
ord  = NULL
rmse = NULL
mae  = NULL
maep = NULL
for (p in 0:12){
  for (d in 0:2){
    for (q in 0:2){
      ord   = rbind(ord,c(p,d,q))
      fit   = Arima(PIB[1:(n-12)],order=c(p,d,q),method="ML")
      aics  = c(aics,fit$aic)
      bics  = c(bics,fit$bic)
      prev  = forecast(fit,h=12)$mean
      error = PIB[(n-11):n]-prev
      rmse  = c(rmse,mean(error^2))
      mae   = c(mae,mean(abs(error)))
      maep  = c(maep,mean(abs(error)/prev))
    }
  }
}
mod = 1:length(aics)
comparison = cbind(ord,aics,bics,rmse,mae,maep)

par(mfrow=c(1,1))
plot(aics,pch=16)
points(bics,col=2,pch=16)

ord.aic =ord[mod[comparison[,4]==min(comparison[,4])],1:3]
ord.bic =ord[mod[comparison[,5]==min(comparison[,5])],1:3]
ord.rmse=ord[mod[comparison[,6]==min(comparison[,6])],1:3]
ord.mae =ord[mod[comparison[,7]==min(comparison[,7])],1:3]
ord.maep=ord[mod[comparison[,8]==min(comparison[,8])],1:3]

rbind(ord.aic,ord.bic,ord.rmse,ord.mae,ord.maep)

# BEST ARIMA MODEL
fit = Arima(PIB[1:(n-12)],order=ord.rmse)
acf(residuals(fit))
Box.test(residuals(fit), lag=24, fitdf=4, type="Ljung")
plot(forecast(fit,h=12))
points((n-11):n,PIB[(n-11):n],col=2,pch=16)



#######################################
# Escolhando a ordem do SARIMA
#######################################
aics = NULL
bics = NULL
ord  = NULL
rmse = NULL
mae  = NULL
maep = NULL
for (p in 1:2)
  for (d in 0:1)
    for (q in 0:2)
      for (P in 0:2)
        for (D in 0:1){
          ord   = rbind(ord,c(p,d,q,P,D,0))
          fit   = Arima(PIB[1:(n-12)],order=c(p,d,q),
                        seasonal=list(order=c(P,D,0),period=12),method="ML")
          aics  = c(aics,fit$aic)
          bics  = c(bics,fit$bic)
          prev  = forecast(fit,h=12)$mean
          error = PIB[(n-11):n]-prev
          rmse  = c(rmse,mean(error^2))
          mae   = c(mae,mean(abs(error)))
          maep  = c(maep,mean(abs(error)/prev))
        }
mod = 1:length(aics)
comparison = cbind(ord,aics,bics,rmse,mae,maep)


names = c("AIC","BIC","RMSE","MAE","MAEP")
par(mfrow=c(2,3))
for (i in 1:5)
  plot(comparison[,6+i],pch=16,xlab="Model",ylab=names[i])

ord.aic =ord[mod[comparison[,7]==min(comparison[,7])][1],1:6]
ord.bic =ord[mod[comparison[,8]==min(comparison[,8])][1],1:6]
ord.rmse=ord[mod[comparison[,9]==min(comparison[,9])][1],1:6]
ord.mae =ord[mod[comparison[,10]==min(comparison[,10])][1],1:6]
ord.maep=ord[mod[comparison[,11]==min(comparison[,11])][1],1:6]

rbind(ord.aic,ord.bic,ord.rmse,ord.mae,ord.maep)

# BEST ARIMA MODEL
fit = Arima(PIB[1:(n-12)],order=ord.rmse[1:3],
            seasonal=list(order=ord.rmse[4:6],period=12),method="ML")

par(mfrow=c(1,1))
plot(forecast(fit,h=12))
points((n-11):n,PIB[(n-11):n],col=2,pch=16)




