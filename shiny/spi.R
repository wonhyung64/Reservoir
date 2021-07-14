# 라이블러리 불러오기
library(readxl)
library(PerformanceAnalytics)


# 데이터 불러오기
setwd("E:/Data/무수저수지")

data = read.csv("진천_강수량_1999-2020.csv")
data = data[1:7677,1:2]
data$관측일 = as.Date(data$관측일)
data$금년일강수량 = as.integer(data$금년일강수량)


# 무강수 시나리오
#data_obs = subset(data,관측일 < '2020-10-01')
#data_sce = subset(data, 관측일 >= '2020-10-01')
#data_sce$금년일강수량 = 0
#data = rbind(data_obs, data_sce)

# 누적합 계산
data = data.frame(date=data$관측일, precip=data$금년일강수량, 
           cum_30=RcppRoll::roll_sum(data$금년일강수량, 30, fill=NA, align="right"),
           cum_60=RcppRoll::roll_sum(data$금년일강수량, 60, fill=NA, align="right"),
           cum_90=RcppRoll::roll_sum(data$금년일강수량, 90, fill=NA, align="right")
           )
data = subset(data, date >= '2000-01-01')


# spi
cal_spi = function(df){
  return(qnorm(pgamma(df+0.00001, shape=a_hat, scale=b_hat)))
}

a_hat = 0.5 / (log(mean(data$cum_30))- mean(log(data$cum_30 + 0.00001))); b_hat = mean(data$cum_30) / a_hat
data$SPI1 = cal_spi(data$cum_30)

a_hat = 0.5 / (log(mean(data$cum_60))- mean(log(data$cum_60 + 0.00001))); b_hat = mean(data$cum_60) / a_hat
data$SPI2 = cal_spi(data$cum_60)

a_hat = 0.5 / (log(mean(data$cum_90))- mean(log(data$cum_90 + 0.00001))); b_hat = mean(data$cum_90) / a_hat
data$SPI3 = cal_spi(data$cum_90)

