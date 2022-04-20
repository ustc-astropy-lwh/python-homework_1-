import requests
import time
from tkinter import*
import re

class get_stock_historical_data():
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
        self.header = {'User-Agent':self.user_agent}
        self.url = "https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={dayfrom}&period2={dayto}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"

    def get_stocktype(self,suffix=".SS"):
        self.suffix = suffix

    def get_stock_code(self,code="600000"):
        self.code = code
        self.code = self.code + self.suffix

    def get_dayfrom(self,dayfrom="2022-04-10"):
        self.dfrom = dayfrom

    def get_dayto(self,dayto="2022-04-15"):
        self.dto = dayto

    def get_SS(self):
        # date begin, like 2022-02-01, translate to timestamp
        self.dfrom = self.dfrom + ' ' + '08:00:00'
        timearray = time.strptime(self.dfrom, "%Y-%m-%d %H:%M:%S")
        timestamp_from = int(time.mktime(timearray))
        # date end, like 2022-02-02, translate to timestamp
        self.dto = self.dto + ' ' + '08:00:00'
        timearray_ = time.strptime(self.dto, "%Y-%m-%d %H:%M:%S")
        timestamp_to = int(time.mktime(timearray_))
        if timestamp_from >= timestamp_to:    # date error:early date larger than late date
            print("date error")
            return None
        url = self.url.format(stock=self.code,dayfrom=timestamp_from,dayto=timestamp_to)    
        response = requests.get(url,headers=self.header)    # request
        response.raise_for_status()
        s = response.text

        # make response.text look better
        s = re.sub(r',' , '\t\t' , s)

        table = response.text.split('\n')    # get a table of stock data, type:str
        for i in range(len(table)):
            table[i] = table[i].split(',')
        self.dict = {}
        for i in range(len(table[0])):    # dictionary stores data
            temp = []    # temporary list
            for j in table[1:] :    # stock data
                if i == 0:
                    temp.append(j[i])    # Date store
                else:
                    temp.append(float(j[i]))    # str-->float
            self.dict[table[0][i]] = temp

        return self.dict, s

if __name__ == '__main__':    # test
    a = get_stock_historical_data()
    a.get_stocktype()
    a.get_stock_code()
    a.get_dayfrom()
    a.get_dayto()
    try:
        r,s = a.get_SS()
        print(r)
    except:
        print("no data")
    



# b = requests.get('https://query1.finance.yahoo.com/v7/finance/download/600000.SS?period1=1649808000&period2=1650240000&interval=1d&events=history&includeAdjustedClose=true',headers=a.header)
# table = b.text
# table = table.split('\n')
# for i in range(len(table)):
#     table[i] = table[i].split(',')

# dict = {}
# for i in range(len(table[0])):    # dictionary stores data
#     temp = []    # temporary list
#     for j in table[1:] :    # stock data
#         if i == 0:
#             temp.append(j[i])    # Date store
#         else:
#             temp.append(float(j[i]))
#     dict[table[0][i]] = temp

# print(dict)