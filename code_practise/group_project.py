import pandas as pd 
import numpy as np

class decision_table:
    '''设定初始参数, 包括lambda, mu, uniform(a,b), 排队人数，价格，顾客数量'''
    def __init__(self, lambda_=0.29, mu_=0.2, a=3.46, b=10.36, threshold=5, price=7, n = 700):
        self.lambda_ = lambda_
        self.mu_ = mu_
        self.a = a
        self.b = b
        self.threshold = threshold
        self.price = price
        self.n = n
        # 初始化表格
        self.table3=pd.DataFrame(columns=['Interarrival Time','Service Time','Arrival Time','WTP',
                                 'Queue Length','Purchase','Service End Time','Departure Time'])
    
    ############################################################
    '''参数修改'''
    def set_price(self, price):
        self.price = price

    def set_lambda(self, lambda_):
        self.lambda_ = lambda_
    
    def set_mu(self, mu_):
        self.mu_ = mu_
    
    def set_ab(self, a, b):
        self.a = a
        self.b = b
    
    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_n(self, n):
        self.n = n

    ############################################################
    '''返回表格'''
    def return_table(self):
        return self.self.table3
    
    '''初始化表格'''
    def _initial_table(self):
        self.table3.loc[0,'Arrival Time']=0
        self.table3.loc[0,'Queue Length']=0
        self.table3.loc[0,'Interarrival Time']=np.random.exponential(1/self.lambda_)
        self.table3.loc[0,'WTP']=np.random.uniform(self.a, self.b)
        self.table3.loc[0,'Purchase']=self.table3.loc[0,'WTP']>=self.price
        if self.table3.loc[0,'Purchase']:
            self.table3.loc[0,'Service Time']=np.random.exponential(1/self.mu_)
            self.table3.loc[0,'Service End Time']=self.table3.loc[0,'Service Time'] + self.table3.loc[0,'Arrival Time']
            self.table3.loc[0,'Departure Time']=self.table3.loc[0,'Service End Time']
        else:
            self.table3.loc[0,'Service Time']=0
            self.table3.loc[0,'Service End Time']=0
            self.table3.loc[0,'Departure Time']= self.table3.loc[0,'Arrival Time']

    
    '''更新表格'''
    def update_table(self):
        self._initial_table()
        for i in range(1, self.n):
        # 已知分布的随机数
            self.table3.loc[i,'Interarrival Time']=np.random.exponential(1/self.lambda_)
            self.table3.loc[i,'Service Time']=np.random.exponential(1/self.mu_)
            self.table3.loc[i,'Arrival Time']=self.table3.loc[i-1,'Arrival Time']+self.table3.loc[i,'Interarrival Time']
            self.table3.loc[i,'WTP']=np.random.uniform(self.a,self.b)

            # 计算队列长度
            self.table3.loc[i,'Queue Length']=0 # 初始化队列长度
            for j in range(i-1, max(i-self.threshold*10, -1), -1):
                if self.table3.loc[j,'Purchase']==1: # 如果前面的顾客购买
                    if self.table3.loc[j,'Departure Time'] > self.table3.loc[i,'Arrival Time']: # 如果前面的顾客离开时间大于当前顾客到达时间
                        self.table3.loc[i,'Queue Length']+=1 # 队列长度加1

        # 判断是否购买
            if self.table3.loc[i,'WTP']>=self.price and self.table3.loc[i,'Queue Length']<=self.threshold:
                self.table3.loc[i,'Purchase']=1
                for j in range(i-1, 0, -1):
                    if self.table3.loc[j,'Purchase']==1:
                        self.table3.loc[i,'Service End Time']=max(self.table3.loc[i,'Arrival Time'],
                                                    self.table3.loc[j,'Departure Time'])+self.table3.loc[i,'Service Time'] # 购买的顾客服务结束时间为到达时间和上一个顾客离开时间的最大值加上服务时间
                        break
                self.table3.loc[i,'Departure Time']=self.table3.loc[i,'Service End Time'] # 购买的顾客离开时间为服务结束时间
            else:
                self.table3.loc[i,'Purchase']=0
                self.table3.loc[i,'Service Time']=0 # 不购买的顾客服务时间为0
                self.table3.loc[i,'Service End Time']=self.table3.loc[i,'Arrival Time'] # 不购买的顾客服务结束时间为到达时间
                self.table3.loc[i,'Departure Time']=self.table3.loc[i,'Arrival Time'] # 不购买的顾客离开时间为到达时间
        return self.table3
    

    ########################################
    
    '''计算顾客数量'''
    def customer_count(self):
        return self.table3['Purchase'].sum()
    
    '''计算总收入'''
    def total_revenue(self):
        return self.customer_count()*self.price

    '''计算平均收入'''
    def average_revenue(self):
        return self.total_revenue()/self.table3.shape[0]
    


    ########################################
    '''计算总顾客数量'''
    def total_revenue_list(self, lower=3.0, upper=10.0, step=0.01):
        revenue = []
        for i in np.arange(lower, upper, step):
            self.set_price(i)
            self.update_table()
            revenue.append(self.total_revenue())
        return revenue
    
    def total_customer_list(self, lower=3.0, upper=10.0, step=0.01):
        customer = []
        for i in np.arange(lower, upper, step):
            self.set_price(i)
            self.update_table()
            customer.append(self.customer_count())
        return customer
    
    def average_revenue_list(self, lower=3.0, upper=10.0, step=0.01):
        revenue = []
        for i in np.arange(lower, upper, step):
            self.set_price(i)
            self.update_table()
            revenue.append(self.average_revenue())
        return revenue
    
    def max_revenue(self):
        return max(self.total_revenue_list())
    
    def max_customer(self):
        return max(self.total_customer_list())
    
############################################   
    def final_results(self, lower=3.0, upper=10.0, step=0.01):
        self.final_DF = pd.DataFrame(columns=['Price', 'Consumer Count', 'Total Revenue', 'Average Revenue'])
        price = np.arange(lower, upper, step)
        rows = []
        for p in price:
            self.set_price(p)
            self.update_table()
            rows.append({
                'Price': p,
                'Consumer Count': self.customer_count(),
                'Total Revenue': self.total_revenue(),
                'Average Revenue': self.average_revenue()
            })
            print(f'Price: {p} done!, Consumer Count: {self.customer_count()}, Total Revenue: {self.total_revenue()}, Average Revenue: {self.average_revenue()}')
        self.final_DF = pd.concat([self.final_DF, pd.DataFrame(rows)], ignore_index=True)
        return self.final_DF
        # consumer_count = self.total_customer_list(lower, upper, step)
        # total_revenue = self.total_revenue_list(lower, upper, step)
        # average_revenue = self.average_revenue_list(lower, upper, step)
        # self.final_DF['Price'] = price    
        # self.final_DF['Consumer Count'] = consumer_count
        # self.final_DF['Total Revenue'] = total_revenue
        # self.final_DF['Average Revenue'] = average_revenue
        # return self.final_DF
    
    def final_plot(self):
        import matplotlib.pyplot as plt
        # 绘制折线图
        plt.figure(figsize=(10, 6))
        plt.plot(self.final_DF['Price'],self.final_DF['Consumer Count'], marker='o', markersize=1, label='Consumer Count')
        plt.plot(self.final_DF['Price'],self.final_DF['Total Revenue'], marker='o', markersize=1, label='Total Revenue')
        plt.plot(self.final_DF['Price'],self.final_DF['Average Revenue'], marker='o', markersize=1, label='Average Revenue')
        # plt.plot.final_DF['Price'],.final_DF['Average Profit'], marker='o', label='Average Profit')

        # 添加标题和标签
        plt.title('Results Analysis')
        plt.xlabel('Price')
        plt.ylabel('Values')
        plt.legend()
        plt.grid(True)
        plt.show()

    def average_revenue_plot(self):
        import matplotlib.pyplot as plt
        
        # set x-axis as self.price
        plt.plot(self.final_DF['Price'], self.final_DF['Average Revenue'])
        plt.xlabel('Price')
        plt.ylabel('Average Revenue')
        plt.title('Average Revenue vs Price')

        plt.show()

    def customer_plot(self):
        import matplotlib.pyplot as plt
        
        plt.plot(self.final_DF['Price'], self.final_DF['Consumer Count'])
        plt.xlabel('Price')
        plt.ylabel('Total Customer')
        plt.title('Total Customer vs Price')

        plt.show()
    
    def revenue_plot(self):
        import matplotlib.pyplot as plt
        
        plt.plot(self.final_DF['Price'], self.final_DF['Total Revenue'])
        plt.xlabel('Price')
        plt.ylabel('Total Revenue')
        plt.title('Total Revenue vs Price')

        plt.show()




if __name__ == '__main__':

    df = decision_table(n = 700)
    df.update_table()
    df.final_results(step=1)
    df.final_plot()