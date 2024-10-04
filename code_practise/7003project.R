# 产出700个值，基于exponential distribution, lambda = 0.29(MLE) ，mu=0.2019(MLE) 
# 别轻易改动这几行
inter_time <- rexp(700, rate=0.29)
hist(inter_time)

service_time <- rexp(700, rate = 0.2019)
hist(service_time)

# 推测wtp的unif 区间，0， 14
wtp<-runif(700, 0, 14) # unifrom distribution
hist(wtp)

########

price <- 7 # 设置价格
# 制作表格
length(cumsum(inter_time))
arr_time <- c(0, cumsum(inter_time))
arr_time <- arr_time[-length(arr_time)]
perchase_or_not <- wtp>price
decision_trans <- data.frame(arr_time, perchase_or_not)
# service time
decision_trans$service_interval <- ifelse(decision_trans$perchase_or_not, service_time, 0)
hist(decision_trans$service_interval)
# service end time，算出service end time
decision_trans$service_end_time <- ifelse(decision_trans$service_interval, decision_trans$arr_time + decision_trans$service_interval, FALSE)
 
pre_time = 0
for (i in 1:nrow(decision_trans)){
  if (decision_trans$service_end_time[i]){
    if (decision_trans$service_end_time[i]< pre_time){
      decision_trans$service_end_time[i] = pre_time + decision_trans$service_interval[i]
    }
    pre_time = decision_trans$service_end_time[i]
  }
}
# queue length（包括正在service的人）,算queue length，若大于5，则改成no purchase
decision_trans$queue_length <- 0
for (i in 2:nrow(decision_trans)){
  for (j in 1:i){
    if (decision_trans$perchase_or_not[j]){
      if (decision_trans$service_end_time[j] > decision_trans$arr_time[i]){
        decision_trans$queue_length[i] = decision_trans$queue_length[i] +1
        if (decision_trans$queue_length[i] > 5){
          decision_trans$perchase_or_not[i] = FALSE
          decision_trans$service_interval[i] = 0
          decision_trans$service_end_time[i] = 0
          decision_trans$queue_length[i] = decision_trans$queue_length[i] - 1
          pre_time = 0
          for (j in 1:nrow(decision_trans)){
            if (decision_trans$service_end_time[j]){
              if (decision_trans$service_end_time[j]< pre_time){
                decision_trans$service_end_time[j] = pre_time + decision_trans$service_interval[j]
              }
              pre_time = decision_trans$service_end_time[j]
            }
          }
        }
      }  
    }
  }
}
# 检查数据
sum(decision_trans$perchase_or_not)
summary(decision_trans)

# 求total revenue
cost = 2.68
profit = price - cost
customer = sum(decision_trans$perchase_or_not)
total_profit = profit * customer
total_revenue = price * customer
total_revenue
total_profit

###########################################
###########################################
###########################################


