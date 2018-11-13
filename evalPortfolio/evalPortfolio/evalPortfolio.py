# Ng Yibin, Dec 2017

import argparse
import numpy as np
import pandas as pd
import utilities as ut
import yaml

from datetime import datetime
from six.moves import urllib
from tabulate import tabulate
from xlrd import open_workbook

# Inputs
#     yr  : list of years
#     eps : list of eps
#     per : list of pe ratio
#     div : list of dividends over the years
# Outputs
#
def compute_fv(curr_yr_eps_est, week52_low, week52_high, yr, eps, per, div, growth_rate, priceA_disc, priceB_disc,
               Nyrs):
    eps_perc_change = [100.0 * (eps1 - eps2) / abs(eps2) for eps1, eps2 in zip(eps, eps[1:])]
    eps_perc_change_mean = np.mean(eps_perc_change)
    print("eps_perc_change = " + str(eps_perc_change))
    print("eps_perc_change_mean = " + str(eps_perc_change_mean))

    per_mean = np.mean(per)
    print("per = " + str(per))
    print("per_mean = " + str(per_mean))

    if len(div) < len(eps):
        div_payout = np.array(div) / np.array(eps[0:len(div)])
    else:
        div_payout = np.array(div[0:len(eps)]) / np.array(eps)
    div_payout_mean = np.mean(div_payout)
    print("div_payout = " + str(div_payout))
    print("div_payout_mean = " + str(div_payout_mean))

    projected_eps_sum, projected_eps = comp_eps_sum_Nyrs(curr_yr_eps_est, eps_perc_change_mean, Nyrs)

    expected_price_Nyrs = projected_eps[-1] * per_mean
    print("curr_yr_eps_est = " + str(curr_yr_eps_est))
    print("projected_eps[-1] = " + str(projected_eps[-1]))
    print("expected_price_Nyrs = " + str(expected_price_Nyrs))

    tot_div_Nyrs = projected_eps_sum * div_payout_mean
    tot_returns_Nyrs = tot_div_Nyrs + expected_price_Nyrs
    intrinsic_val = comp_intrinsic_val(tot_returns_Nyrs, growth_rate, Nyrs)
    print("tot_div_Nyrs = " + str(tot_div_Nyrs))
    print("tot_returns_Nyrs = " + str(tot_returns_Nyrs))
    print("intrinsic_val = " + str(intrinsic_val))

    priceA = priceA_disc * intrinsic_val
    priceB = week52_low + priceB_disc * (week52_high - week52_low)
    tgt_price = min(priceA, priceB)
    print("tgt_price = " + str(tgt_price))
    # return priceA
    return tgt_price, priceA, priceB


def comp_eps_sum_Nyrs(curr_yr_eps_est, eps_perc_change_mean, N):
    projected_eps = []
    for i in range(N):
        projected_eps.append((1 + eps_perc_change_mean / 100) ** (i + 1) * curr_yr_eps_est)
    projected_eps_sum = sum(projected_eps)
    # print "curr_yr_eps_est = " + str(curr_yr_eps_est)
    # print "projected_eps = " + str(projected_eps)
    # print "projected_eps_sum = " + str(projected_eps_sum)

    return projected_eps_sum, projected_eps


def comp_intrinsic_val(tot_returns_Nyrs, growth_rate, N):
    return tot_returns_Nyrs / ((1 + growth_rate) ** (N))


def read_file(file):
    with open(file) as f:
        stock_code = f.readline()
        yr = []
        eps = []
        per = []
        div = []
        for line in f:
            x = line.split(",")
            if x[0] != " ": yr.append(int(x[0]))
            if x[1] != " ": eps.append(float(x[1]))
            if x[2] != " ": per.append(float(x[2]))
            if x[3] != " ": div.append(float(x[3]))
            # print yr
            # print eps
            # print per
            # print div

    return (stock_code, yr, eps, per, div)


def read_file_xlsx(filename_xlsx, growth_rate, priceA_disc, priceB_disc, Nyrs, portfolio_stocks, sFairValue):
    name_list = []
    tgt_price_list = []
    price_list = []
    perc_to_increase_list = []
    year_last_update_list = []
    report_release = []
    priceA_list = []
    div_list = []
    print("filename_xlsx = " + filename_xlsx)
    wb = open_workbook(filename_xlsx)
    for s in wb.sheets():
        if s.name in portfolio_stocks:
            yr = []
            eps = []
            per = []
            div = []
            year_low = 0
            year_high = 0
            print('---------------------------------------------------- Sheet: ' + s.name)
            stock_code = s.cell(0, 0).value
            print('stock code = ' + stock_code)
            for i in range(3, 13):
                if s.cell(i, 4).value != '':
                    yr.append(s.cell(i, 4).value)
                if s.cell(i, 5).value != '':
                    eps.append(s.cell(i, 5).value)
                if s.cell(i, 9).value != '':
                    per.append(s.cell(i, 9).value)
                if s.cell(i, 10).value != '':
                    div.append(s.cell(i, 10).value)

            if s.cell(13, 4).value != '':
                yr.append(s.cell(13, 4).value)
            if s.cell(13, 5).value != '':
                eps.append(s.cell(13, 5).value)
            if s.cell(16, 1).value != '':
                year_low = s.cell(16, 1).value
            if s.cell(17, 1).value != '':
                year_high = s.cell(17, 1).value

            print("yr = " + str(yr))
            print("eps = " + str(eps))
            print("per = " + str(per))
            print("div = " + str(div))
            print("year_low = " + str(year_low))
            print("year_high = " + str(year_high))

            stk = ut.Utilities(stock_code)
            # stk_price = float(stk.get_price())
            # stk_price = float(stk.get_price_csv(sFairValue))
            # stk_year_low = float(stk.get_year_low())
            # if stk_year_low == 0:  # Unable to get year low from quandl
            #     print("Unable to get year low from quandl!!!!")
            #     stk_year_low = year_low
            # stk_year_high = float(stk.get_year_high())
            # if stk_year_high == 0:  # Unable to get year high from quandl
            #     print("Unable to get year high from quandl!!!!")
            #     stk_year_high = year_high
            (stk_year_low, stk_year_high, stk_price) = stk.parse()
            print("stk_year_low = " + str(stk_year_low))
            print("stk_year_high = " + str(stk_year_high))
            print("stk_price = " + str(stk_price))
            tgt_price, priceA, priceB = compute_fv(float(eps[0]), stk_year_low,
                                                   stk_year_high, yr, eps, per, div, growth_rate,
                                                   priceA_disc, priceB_disc, Nyrs)

            try:
                perc_to_increase = (float(tgt_price) - stk_price) / stk_price
            except TypeError:
                perc_to_increase = -1
                print("TypeError! tgt_price = " + str(tgt_price) + ", share price = " + str(stk_price))

            name_list.append(str(s.name))
            tgt_price_list.append(tgt_price)
            price_list.append(stk_price)
            perc_to_increase_list.append(perc_to_increase)
            year_last_update_list.append(yr[0])
            report_release.append(s.cell(1, 0))
            priceA_list.append(priceA)
            div_list.append(div[0])
            # else:
            #     print("Incomplete data! Share(" + str(stock_code) + ") = " + str(stk))

    return (name_list, tgt_price_list, price_list, perc_to_increase_list, year_last_update_list, report_release,
            priceA_list, div_list)



# # Try to get stk from yahoo
# def get_stk_yahoo(stock_code):
#     stk = []
#     try:
#         stk = Share(stock_code)
#         # stk = []
#     except:
#         print("Error getting stock info!")
#     return stk


def comp_cagr_benchmark_list(stockCode, date_bought_list, price, vol_list, price_benchmark_on_date_bought, filename):
    """
    Given stock, return the CAGR till now
    Input
      stockCode		: e.g. ES3.SI
      dateBought	: e.g. "2014-05-23"
      price			: price of the stock now
      vol_list		: volume bought
      price_benchmark_on_date_bought : price of benchmark on date bought
      filename                       : filename of csv file which contains stock prices
    Output
      cagr      : compound annual growth rate
    """
    cagr_list = []
    market_value = [price * i for i in vol_list]
    tot = sum(market_value)
    print("stockCode = " + str(stockCode))
    print("date_bought_list = " + str(date_bought_list))
    print("price = " + str(price))
    print("vol_list = " + str(vol_list))
    for i in range(len(date_bought_list)):
        diff = datetime.now() - datetime.strptime(date_bought_list[i], '%Y-%m-%d')
        years = diff.days / 365.0
        stk = ut.Utilities(stockCode)
        # e.g. [{'Volume': '117000', 'Symbol': 'ES3.SI', 'Adj_Close': '3.11', 'High': '3.32', 'Low': '3.31', 'Date': '2014-05-23', 'Close': '3.31', 'Open': '3.31'}]

        try:
            # stk_dict = stk.get_historical(date_bought_list[i], date_bought_list[i])
            # print 'stk_dict = ' + str(stk_dict)
            # starting_value = float(stk_dict[0]['Adj_Close'])
            starting_value = price_benchmark_on_date_bought[i]
            ending_value = float(stk.get_price_csv(filename))
            cagr = market_value[i] / tot * ((float(ending_value) / starting_value) ** (1 / float(years)) - 1) * 100
            cagr_list.append(cagr)
        except:
            cagr_list.append(float("inf"))

    return sum(cagr_list)


def print_tables(portfolio, name_list, tgt_price_list, price_list, perc_to_increase_list, year_last_update_list,
                 report_release, priceA_list, div_list, stock_code_benchmark, path_div_cash, path_div_stock,
                 path_quotes, path_out):
    """
    Print out the tables
    """
    print("-------------------------------------- print_tables")
    d = {'tgt_price': [], 'price': [], 'perc_to_increase': [], 'year_last_update': [], 'total_cost': [],
         'market_value': [], 'profit': [], \
         'report_release': [], 'priceA': [], 'div_yield': [], 'date_bought': [], 'period_bought': [], 'cagr': [],
         'div_per_year': [], 'profit_inc_div_drp': [], \
         'div_collected': [], 'stock_div_collected': [], 'cagr_inc_div_drp': [], 'cagr_benchmark': [],
         'cagr_benchmark_status': [], 'breakeven_price': [], \
         'breakeven_price_status': [], 'price_bought': [], 'date_div_paid': [], 'price_change_pct': []}
    portfolio_name_list = []
    for i in range(len(name_list)):
        if name_list[i] in portfolio:
            print("===================================================name_list[i] = " + str(name_list[i]))

            # Comp dividends
            div_name_list = [path_div_cash + name_list[i] + ".txt"]
            stock_div_name_list = [path_div_stock + name_list[i] + ".txt"]
            j = 2
            while j <= len(portfolio[name_list[i]]['price_bought']):
                div_name_list.append(path_div_cash + name_list[i] + str(j) + ".txt")
                stock_div_name_list.append(path_div_stock + name_list[i] + str(j) + ".txt")
                j = j + 1
            print('div_name_list = ' + str(div_name_list))
            div_collected_list = comp_div_list(div_name_list)
            div = sum(div_collected_list)
            d['div_collected'].append(div)
            stock_div_collected_list = comp_stock_div_list(stock_div_name_list)
            stock_div = sum(stock_div_collected_list)
            d['stock_div_collected'].append(stock_div)
            print("stock_div_collected = " + str(d['stock_div_collected']))

            portfolio_name_list.append(name_list[i])
            d['year_last_update'].append(int(year_last_update_list[i]))
            d['tgt_price'].append(tgt_price_list[i])
            d['price'].append(price_list[i])
            d['perc_to_increase'].append(perc_to_increase_list[i] * 100)
            d['total_cost'].append(
                comp_tot_cost(portfolio[name_list[i]]['price_bought'], portfolio[name_list[i]]['quantity'], portfolio[name_list[i]]['buy_admin_fee']))
            d['market_value'].append(
                comp_market_value(float(price_list[i]), portfolio[name_list[i]]['quantity'], portfolio[name_list[i]]['buy_admin_fee']))
            d['profit'].append(comp_profit(float(price_list[i]), portfolio[name_list[i]]['price_bought'], portfolio[name_list[i]]['quantity'],
                                           portfolio[name_list[i]]['buy_admin_fee']))
            d['report_release'].append(report_release[i])
            d['priceA'].append(priceA_list[i])
            d['div_yield'].append(float(div_list[i]) / float(price_list[i]) * 100)
            d['date_bought'].append(', '.join(portfolio[name_list[i]]['date_bought']))
            d['period_bought'].append(str(comp_period_bought(portfolio[name_list[i]]['date_bought'])).strip('[]'))
            d['cagr'].append(comp_cagr(float(price_list[i]), portfolio[name_list[i]]['price_bought'], portfolio[name_list[i]]['date_bought'],
                                       portfolio[name_list[i]]['quantity']))
            d['div_per_year'].append(
                comp_div_per_year(float(div_list[i]), portfolio[name_list[i]]['quantity'], stock_div_collected_list))
            d['price_bought'].append(str(portfolio[name_list[i]]['price_bought']).strip('[]'))

            # Compute % change between price bought at first buy and price now
            price_bought = float(d['price_bought'][-1].split(",")[0])
            d['price_change_pct'].append(100.0*(d['price'][-1]-price_bought)/price_bought)

            d['date_div_paid'].append(', '.join(portfolio[name_list[i]]['date_div_paid']))

            d['profit_inc_div_drp'].append(
                comp_profit_inc_div_drp(float(price_list[i]), portfolio[name_list[i]]['price_bought'], portfolio[name_list[i]]['quantity'], \
                                        stock_div_collected_list, portfolio[name_list[i]]['buy_admin_fee'], div))

            breakeven_price = comp_breakeven_price(portfolio[name_list[i]]['price_bought'], portfolio[name_list[i]]['quantity'],
                                                   stock_div_collected_list, \
                                                   portfolio[name_list[i]]['buy_admin_fee'], div)
            d['breakeven_price'].append(breakeven_price)

            breakeven_price_status = 'Yes' if float(price_list[i]) >= breakeven_price else 'No'
            d['breakeven_price_status'].append(breakeven_price_status)

            cagr_inc_div_drp = comp_cagr_inc_div_drp(float(price_list[i]), portfolio[name_list[i]]['price_bought'],
                                                     portfolio[name_list[i]]['quantity'], \
                                                     portfolio[name_list[i]]['date_bought'], stock_div_collected_list,
                                                     div_collected_list)
            d['cagr_inc_div_drp'].append(cagr_inc_div_drp)
            print("d[cagr_inc_div_drp] = " + str(d['cagr_inc_div_drp']))

            cagr_benchmark = comp_cagr_benchmark_list(stock_code_benchmark, portfolio[name_list[i]]['date_bought'],
                                                      float(price_list[i]), portfolio[name_list[i]]['quantity'],
                                                      portfolio[name_list[i]]['price_of_benchmark_on_date_bought'], path_quotes)
            d['cagr_benchmark'].append(cagr_benchmark)

            cagr_benchmark_status = 'Yes' if cagr_inc_div_drp >= cagr_benchmark else 'No'
            d['cagr_benchmark_status'].append(cagr_benchmark_status)
            # print d

    df = pd.DataFrame(d, index=portfolio_name_list)
    df['weightage'] = df['market_value'] / df['market_value'].sum()
    print("\n")
    df = df.sort_values(by='perc_to_increase', ascending=False)
    print(tabulate(df[['tgt_price', 'priceA', 'perc_to_increase']], headers='keys', tablefmt='psql'))
    print(tabulate(df[['price_bought', 'price', 'price_change_pct', 'breakeven_price', 'breakeven_price_status']], headers='keys', tablefmt='psql'))
    df = df.sort_values(by='profit_inc_div_drp', ascending=False)
    print(tabulate(df[['total_cost', 'market_value', 'weightage', 'profit', 'div_collected', 'profit_inc_div_drp']], headers='keys', tablefmt='psql'))
    df = df.sort_values(by='div_yield', ascending=False)
    print(tabulate(df[['div_yield', 'div_per_year', 'div_collected', 'stock_div_collected', 'date_div_paid']], headers='keys', tablefmt='psql'))
    df = df.sort_values(by='cagr_inc_div_drp', ascending=False)
    print(tabulate(df[['period_bought', 'cagr', 'cagr_inc_div_drp', 'cagr_benchmark', 'cagr_benchmark_status']], headers='keys', tablefmt='psql'))
    df = df.sort_values(by='period_bought', ascending=False)
    print(tabulate(df[['date_bought', 'period_bought', 'report_release', 'year_last_update']], headers='keys', tablefmt='psql'))

    # Print overall results of the portfolio in a df
    d_pf = {"Total portfolio cost": df['total_cost'].sum(),
            "Total portfolio market value (mark to market)": df['market_value'].sum(),
            "Total profit (mark to market)": df['profit'].sum(),
            "Div per month": df['div_per_year'].sum() / 12.0,
            "Total dividends collected till now": df['div_collected'].sum(),
            "Total profit (mark to market) with dividends and drp included": df['profit_inc_div_drp'].sum(),
            "Weighted cagr": sum(df['cagr'] * df['weightage']),
            "Weighted cagr with dividends and drp included": sum(df['cagr_inc_div_drp'] * df['weightage']),
            "Weighted cagr for benchmark": sum(df['cagr_benchmark'] * df['weightage']),
            "No. of stocks": len(df.index),
            "Market value per stock if balanced": float(df['market_value'].sum()) / len(df.index)
            }
    df_pf = pd.DataFrame(d_pf, index=[0])
    cols = ['Total portfolio cost',
            'Total portfolio market value (mark to market)',
            'Total profit (mark to market)',
            'Div per month',
            'Total dividends collected till now',
            'Total profit (mark to market) with dividends and drp included',
            'Weighted cagr',
            'Weighted cagr with dividends and drp included',
            'Weighted cagr for benchmark',
            'No. of stocks',
            'Market value per stock if balanced'
           ]
    print(tabulate(df_pf[cols], headers='keys', tablefmt='psql'))
    df_pf.to_csv(path_out, columns=cols, index=False)

    print("\nTotal portfolio cost = " + str(df['total_cost'].sum()))
    print("Total portfolio market value (mark to market) = " + str(df['market_value'].sum()))
    print("Total profit (mark to market) = " + str(df['profit'].sum()))
    print("Div per month = " + str(df['div_per_year'].sum() / 12.0))
    print("Total dividends collected till now = " + str(df['div_collected'].sum()))
    print("Total profit (mark to market) with dividends and drp included = " + str(df['profit_inc_div_drp'].sum()))
    print("Weighted cagr = " + str(sum(df['cagr'] * df['weightage'])))
    print("Weighted cagr with dividends and drp included = " + str(sum(df['cagr_inc_div_drp'] * df['weightage'])))
    print("Weighted cagr for benchmark = " + str(sum(df['cagr_benchmark'] * df['weightage'])))
    print("No. of stocks = " + str(len(df.index)))
    print("Market value per stock if balanced = " + str(float(df['market_value'].sum()) / len(df.index)))


def comp_tot_cost(price_bought_list, vol_list, admin_fee_list):
    """
    return total cost of buying this stock, including buying admin fees
    """
    return sum(i[0] * i[1] + i[2] for i in zip(price_bought_list, vol_list, admin_fee_list))


def comp_market_value(price, vol_list, admin_fee_list):
    """
    return current market value of this stock, after deducting selling admin fees
    """
    return sum(price * i[0] - i[1] for i in zip(vol_list, admin_fee_list))


def comp_profit(price, price_bought_list, vol_list, admin_fee_list):
    """
    return current market value - total cost of buying this stock, after deduct admin fees, without DRP and div
    """
    return comp_market_value(price, vol_list, admin_fee_list) - comp_tot_cost(price_bought_list, vol_list,
                                                                              admin_fee_list)


def comp_period_bought(date_bought_list):
    """
    return period bought for each stock
    """
    years_list = [(datetime.now() - datetime.strptime(d, '%Y-%m-%d')).days / 365.0 for d in date_bought_list]
    return years_list


def comp_cagr(price, price_bought_list, date_bought_list, vol_list):
    """
    return cagr for each stock, without considering div and drp and admin fees
    """
    cagr_list = []
    years_list = comp_period_bought(date_bought_list)
    market_value = [price * i for i in vol_list]
    tot = sum(market_value)
    for i in range(len(price_bought_list)):
        starting_value = price_bought_list[i]
        ending_value = price
        cagr_list.append(
            market_value[i] / tot * ((float(ending_value) / starting_value) ** (1 / float(years_list[i])) - 1) * 100)
    return sum(cagr_list)


def comp_div_per_year(div, vol_list, DRP_list):
    """
    return total dividends for this stock, including stocks from DRP
    """
    return sum(div * (i[0] + i[1]) for i in zip(vol_list, DRP_list))


def comp_div_list(name_list):
    """
    Given stock name, return cash dividends collected
    Inputs
        name_list: e.g.  ['Dividends/Cash/UOL.txt']
    Outputs
        div_list: e.g. [100]
    """
    div_list = []
    for name in name_list:
        sum = 0
        print("name = " + name)
        try:
            with open(name) as f:
                for line in f:
                    x = line.strip().replace("\n", "").split(",")
                    # print "name = " + str(name) + ", x = " + str(x)
                    if (len(x) == 2 and x[1] != "" and x[1] != " "):
                        sum = sum + float(x[1])
        except IOError:
            print("File not found! file = " + name)
        div_list.append(sum)
    return div_list


def comp_stock_div_list(name_list):
    """
    Given stock name, return stock dividends collected
    Inputs
        name_list: e.g.  ['Dividends/Stock/UOL.txt']
    Outputs
        div_list: e.g. [100]
    """
    div_list = []
    for name in name_list:
        sum = 0
        try:
            with open(name) as f:
                for line in f:  # e.g. line = 23-09-2014,34
                    x = line.strip().replace("\n", "").split(",")
                    if (len(x) == 2 and x[1] != "" and x[1] != " "):
                        sum = sum + int(x[1])
        except IOError:
            print("File not found! file = " + name)
        div_list.append(sum)
    return div_list


def comp_profit_inc_div_drp(price, price_bought_list, vol_list, DRP_list, admin_fee_list, div):
    """
    return current market value - total cost of buying this stock, after deduct admin fees, with DRP and div
    """
    vol_DRP_list = [i[0] + i[1] for i in zip(vol_list, DRP_list)]
    return comp_market_value(price, vol_DRP_list, admin_fee_list) - comp_tot_cost(price_bought_list, vol_list,
                                                                                  admin_fee_list) + div


def comp_breakeven_price(price_bought_list, vol_list, DRP_list, admin_fee_list, div):
    """
    return breakeven price of this stock
    """
    vol_DRP_sum = sum(i[0] + i[1] for i in zip(vol_list, DRP_list))
    return (sum(i[0] * i[1] + 2 * i[2] for i in zip(price_bought_list, vol_list, admin_fee_list)) - div) / vol_DRP_sum


def comp_cagr_inc_div_drp(price, price_bought_list, vol_list, date_bought_list, DRP_list, div_list):
    """
    return cagr for each stock, including div and drp
    """
    cagr_list = []
    years_list = comp_period_bought(date_bought_list)
    market_value = [price * i for i in vol_list]
    tot = sum(market_value)
    for i in range(len(price_bought_list)):
        starting_value = price_bought_list[i] * vol_list[i]
        ending_value = price * (vol_list[i] + DRP_list[i]) + div_list[i]
        cagr_list.append(
            market_value[i] / tot * ((float(ending_value) / starting_value) ** (1 / float(years_list[i])) - 1) * 100)
    # print "i = " + str(i)
    # print "price = " + str(price)
    # print "vol_list = " + str(vol_list)
    # print "DRP_list = " + str(DRP_list)
    # print "div_list = " + str(div_list)
    # print "starting_value = " + str(starting_value)
    # print "ending_value = " + str(ending_value)
    # print "market_value = " + str(market_value)
    # print "tot = " + str(tot)
    return sum(cagr_list)

def get_date(filename):
    """
    Get date from csv file
    :param filename:
    :return:
    """
    df = pd.read_csv(filename, sep=",")
    date = df.iloc[0]['Date']
    print("date = " + date)
    dt = datetime.strptime(date, '%m/%d/%y')
    return dt.strftime("%Y%m%d")

if __name__ == "__main__":
    #### Input Params ###########################
    path_config = "../conf/config.yml"
    #############################################

    with open(path_config, 'r') as f:
        config = yaml.load(f)
    print("config = " + str(config))

    parser = argparse.ArgumentParser(description='Compute fair value of stocks.')
    parser.add_argument('filename', help='Enter the filename here.')
    parser.add_argument('country', help='e.g. SGP or USA.')
    parser.add_argument('--Nyrs', type=int, help='EPS will be projected into Nyrs years.')
    args = parser.parse_args()
    print("args.filename = " + str(args.filename))
    print("args.country = " + str(args.country))
    print("args.Nyrs = " + str(args.Nyrs))

    # Get current date
    dt = datetime.today().strftime('%Y%m%d')
    print("dt = " + dt)

    if args.country == "SGP":
        with open(config['path_portfolio'], 'r') as f:
            portfolio = yaml.load(f)

        (name_list, tgt_price_list, price_list, perc_to_increase_list,
         year_last_update_list, report_release, priceA_list, div_list) = \
            read_file_xlsx(args.filename, config['growth_rate'], config['priceA_disc'], config['priceB_disc'],
                           config['Nyrs'], portfolio.keys(), config['path_quotes'])

        print_tables(portfolio, name_list, tgt_price_list, price_list, perc_to_increase_list, year_last_update_list,
                     report_release, priceA_list, div_list, config['stock_code_benchmark'], config['path_div_cash'],
                     config['path_div_stock'], config['path_quotes'], config['path_out_SGP']+dt+".txt")
    elif args.country == "SGP_oneFourth":
        with open(config['path_portfolio_SGP_oneFourth'], 'r') as f:
            portfolio_SGP_oneFourth = yaml.load(f)

        (name_list, tgt_price_list, price_list, perc_to_increase_list,
         year_last_update_list, report_release, priceA_list, div_list) = \
            read_file_xlsx(args.filename, config['growth_rate'], config['priceA_disc'], config['priceB_disc'],
                           config['Nyrs'], portfolio_SGP_oneFourth.keys(), config['path_quotes'])

        print_tables(portfolio_SGP_oneFourth, name_list, tgt_price_list, price_list, perc_to_increase_list,
                     year_last_update_list, report_release, priceA_list, div_list, config['stock_code_benchmark'],
                     config['path_div_cash'], config['path_div_stock'], config['path_quotes'],
                     config['path_out_SGP_oneFourth']+dt+".txt")
    elif args.country == "USA":
        with open(config['path_portfolio_USA'], 'r') as f:
            portfolio_USA = yaml.load(f)

        (name_list, tgt_price_list, price_list, perc_to_increase_list,
         year_last_update_list, report_release, priceA_list, div_list) = \
            read_file_xlsx(args.filename, config['growth_rate'], config['priceA_disc'], config['priceB_disc'],
                           config['Nyrs'], portfolio_USA.keys(), config['path_quotes_USA'])

        print_tables(portfolio_USA, name_list, tgt_price_list, price_list, perc_to_increase_list, year_last_update_list,
                     report_release, priceA_list, div_list, config['stock_code_benchmark_USA'],
                     config['path_div_cash_USA'], config['path_div_stock_USA'], config['path_quotes_USA'],
                     config['path_out_USA']+dt+".txt")
    else:
        print("Error! No such country!")