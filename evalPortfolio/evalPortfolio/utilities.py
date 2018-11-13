# Ng Yibin, Sep 2017

import datetime
import pandas_datareader.data as web
import pandas as pd
import quandl
import requests
import json

from bs4 import BeautifulSoup
from collections import OrderedDict
from lxml import html
from time import sleep

quandl.ApiConfig.api_key = "<YOUR-API-KEY>"

class Utilities:
    """
    Utilities to e.g. get stock price
    """
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def get_price(self):
        """
        Get the current stock price
        """
        price = 0.01
        # try:
        # start = datetime.date.today() - datetime.timedelta(1)
        # end = datetime.date.today() - datetime.timedelta(1)
        # f = web.DataReader(self.stock_code, 'yahoo', start, end)
        # print("f = " + str(f))
        # price = f.ix[start.strftime("%Y-%m-%d")]['Close']
        # except:
        #     print("Error! Cannot get stock price!")

        try:
            f = quandl.get("WIKI/" + self.stock_code, rows=1) # Get latest stock price
            price = f.iloc[0]['Adj. Close']
        except Exception as e:
            print("Error! Cannot get stock price! Stock: " + self.stock_code + ", Quandl error: " + str(e))
        return price

    def get_price_pd(self):
        """
        Get the current stock price using pandas
        :return: stock price
        """
        start = datetime.datetime(2018,1,1)
        end = datetime.datetime.now()
        df = web.DataReader(self.stock_code, 'yahoo', start, end)
        return df.iloc[-1:]['Adj Close'].values[0]


    def get_price_csv(self, filename):
        """
        Get the current stock price from a csv file
        :param filename:
        :return: price
        """
        df = pd.read_csv(filename, sep=",")
        # print(df)
        df_stk = df[df['Symbol']==self.stock_code]
        return df_stk.iloc[0]['Current Price']

    def get_earnings_share(self):
        """
        Get earnings per share
        :return: earnings per share
        """
        return 0

    def get_year_low(self):
        """
        Get year low of the stock
        :return:
        """
        low = 0
        try:
            f = quandl.get("WIKI/" + self.stock_code, rows=252) # Get latest stock price
            low = min(f['Adj. Close'])
        except:
            print("Error! Cannot get year low! Stock: " + self.stock_code)
        print(self.stock_code + " low = " + str(low))
        return low

    def get_year_low_pd(self):
        """
        Get year low of stock using pandas
        Sometimes may fail
        :return:
        """
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=365)
        df = web.DataReader(self.stock_code, 'yahoo', start, end)
        return df['Adj Close'].min()

    def get_year_high(self):
        """
        Get year high of the stock
        :return:
        """
        high = 0
        try:
            f = quandl.get("WIKI/" + self.stock_code, rows=252)  # Get latest stock price
            high = max(f['Adj. Close'])
        except:
            print("Error! Cannot get year high! Stock: " + self.stock_code)
        print(self.stock_code + " high = " + str(high))
        return high

    def get_year_high_pd(self):
        """
        Get year high of the stock using pandas
        Sometimes may fail
        :return:
        """
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=365)
        df = web.DataReader(self.stock_code, 'yahoo', start, end)
        return df['Adj Close'].max()

    def parse(self):
        """
        Parse yahoo finance webpage
        :return:
        """
        # url = "http://finance.yahoo.com/quote/%s?p=%s" % (self.stock_code, self.stock_code)
        url = "https://finance.yahoo.com/quote/%s" % (self.stock_code)
        response = requests.get(url, verify=False)
        # print(response.status_code) # 200 means ok
        # print(response.url)
        # print(response.text)
        soup = BeautifulSoup(response.text, "lxml")
        # print("soup = " + str(soup))
        # print("soup.title = " + str(soup.title))
        # print(soup.findAll(text='52 Week Range')[0].parent.parent.parent)

        # Find year low and year high
        y = soup.findAll('td', attrs={'class': 'Ta(end) Fw(b) Lh(14px)', 'data-test': "FIFTY_TWO_WK_RANGE-value"})[0]
        year_low_high = y.text.split(" - ")
        year_low_high = [float(x.replace(',', '')) for x in year_low_high]

        # Find current price
        # <span class="Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)" data-reactid="21">206.37</span>
        y = soup.findAll('span', attrs={'class': 'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)', 'data-reactid': "21"})[0]
        # print("y = "  + str(y.text))

        return year_low_high + [float(y.text.replace(',', ''))]


if __name__ == "__main__":
    #### Input params ###########
    # stock_code = "AAPL"
    # stock_code = "SPGI"
    # stock_code = "VTI"
    # filename = "../data/quotes_USA.csv"

    # stock_code = "AU8U.SI" # doesn't work
    stock_code = "D01.SI"
    # filename = "../data/sFairValue_SGP.csv"
    #############################

    print("stock_code = " + stock_code)

    ut = Utilities(stock_code)

    # print("ut.get_price() = " + str(ut.get_price()))
    # print("ut.get_price_csv(filename) = " + str(ut.get_price_csv(filename)))
    # print("ut.get_price_pd() = " + str(ut.get_price_pd()))

    # Get year low of stock
    # print("ut.get_year_low_pd() = " + str(ut.get_year_low_pd())) # Unable to read URL

    # Get year high of stock
    # print("ut.get_year_high_pd() = " + str(ut.get_year_high_pd())) # Unable to read URL

    # Get year high and low of stock using webscraping
    (year_low, year_high, price) = ut.parse()
    print("year_low = " + str(year_low))
    print("year_high = " + str(year_high))
    print("price = " + str(price))
