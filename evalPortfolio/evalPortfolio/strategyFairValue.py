# Ng Yibin, Dec 2017

import argparse
import numpy as np
import pandas as pd
import utilities as ut

from datetime import datetime, timedelta
from tabulate import tabulate
from xlrd import open_workbook

# Inputs
#     yr  : list of years
#     eps : list of eps
#     per : list of pe ratio
#     div : list of dividends over the years
# Outputs
#
def compute_fv(curr_yr_eps_est, week52_low, week52_high, yr, eps, per, div, growth_rate, priceA_disc, priceB_disc, Nyrs):
    eps_perc_change = [100.0 * (eps1 - eps2) / abs(eps2) for eps1, eps2 in zip(eps, eps[1:])]
    eps_perc_change_mean = np.mean(eps_perc_change)
    print("eps_perc_change = " + str(eps_perc_change))
    print("eps_perc_change_mean = " + str(eps_perc_change_mean))

    print("per = " + str(per))
    per_mean = np.mean(per)
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
    print("week52_low = " + str(week52_low))
    print("week52_high = " + str(week52_high))
    print("priceA = " + str(priceA))
    print("priceB = " + str(priceB))
    print("tgt_price = " + str(tgt_price))
    # return priceA
    return tgt_price, priceA, priceB


def comp_eps_sum_Nyrs(curr_yr_eps_est, eps_perc_change_mean, N):
    projected_eps = []
    for i in range(N):
        projected_eps.append((1 + eps_perc_change_mean / 100) ** (i + 1) * curr_yr_eps_est)
    projected_eps_sum = sum(projected_eps)
    print("curr_yr_eps_est = " + str(curr_yr_eps_est))
    print("projected_eps = " + str(projected_eps))
    print("projected_eps_sum = " + str(projected_eps_sum))

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


def read_file_xlsx(filename_xlsx, growth_rate, priceA_disc, priceB_disc, Nyrs, sFairValue):
    '''

    :param filename_xlsx:
    :param growth_rate:
    :param priceA_disc:
    :param priceB_disc:
    :param Nyrs:
    :param sFairValue:
    :return:
    '''
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
        # if stk_price == 0.01:           # Unable to get price from quandl
        # stk_price = float(stk.get_price_csv(sFairValue))
        # stk_year_low = float(stk.get_year_low())
        # if stk_year_low == 0:           # Unable to get year low from quandl
        #     stk_year_low = year_low
        # stk_year_high = float(stk.get_year_high())
        # if stk_year_high == 0:          # Unable to get year high from quandl
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
            print("TypeError! tgt_price = " + str(tgt_price) + ", share price = " + str(stk.get_price()))

        name_list.append(str(s.name))
        tgt_price_list.append(tgt_price)
        price_list.append(stk_price)
        perc_to_increase_list.append(perc_to_increase)
        year_last_update_list.append(yr[0])
        report_release.append(s.cell(1, 0).value)
        priceA_list.append(priceA)
        div_list.append(div[0])
        # except:
        #     print("Incomplete data! ")

    return (name_list, tgt_price_list, price_list, perc_to_increase_list, year_last_update_list, report_release,
            priceA_list, div_list)

def get_is_updated(year_last_update, report_release, stock):
    """
    Determine if EPS metrics require updating
    Return true if EPS metrics require updating, false otherwise
    :return:
    """
    # print(stock)
    nowDt = datetime.now()
    currUpdateDate = report_release.split(".")[0] + " " + str(int(year_last_update))
    currUpdateDt = datetime.strptime(currUpdateDate, '%d %b %Y')
    fyEndDate = report_release.split(" ")[4] + " " + report_release.split(" ")[5] + " " + str(int(year_last_update))
    fyEndDt = datetime.strptime(fyEndDate, '%d %b %Y')
    if fyEndDt.month > currUpdateDt.month:
        # print(fyEndDt.month, currUpdateDt.month)
        nextUpdateDt = currUpdateDt + timedelta(days=365*2)
        # print(nextUpdateDt)
    else:
        nextUpdateDt = currUpdateDt + timedelta(days=365)

    if (nowDt > nextUpdateDt):
        return False
    else:
        return True


if __name__ == "__main__":
    #### Input Params ###########################
    # filenames = ['ARA.txt', 'AscendasR.txt']
    # filename_xlsx = "StrategyFairValue_SGX.xlsx"
    # filename_xlsx = "test.xlsx"
    Nyrs = 10
    growth_rate = 0.15
    priceA_disc = 0.75
    priceB_disc = 0.33
    #############################################

    parser = argparse.ArgumentParser(description='Compute fair value of stocks.')
    parser.add_argument('filename', help='Enter the filename here.')
    parser.add_argument('path_quotes', help='Filename of the file that contains stock prices.')
    parser.add_argument('--Nyrs', type=int, help='EPS will be projected into Nyrs years.')
    # parser.add_argument('--growth_rate', type = float, help = 'Growth rate of EPS.')
    # parser.add_argument('--priceA_disc', type = float, help = 'e.g If priceA_disc is 0.75, tgt price A is 0.75 of intrinsic value.')
    # parser.add_argument('--priceB_disc', type = float, help = 'tgt price B is e.g. 33% of (week52_high - week52_low) + week52_low.')
    args = parser.parse_args()
    print(args.filename)
    print(args.Nyrs)
    # print args.growth_rate
    # print args.priceA_disc
    # print args.priceB_disc

    filename_xlsx = args.filename
    path_quotes = args.path_quotes

    (name_list, tgt_price_list, price_list, perc_to_increase_list, year_last_update_list, report_release, priceA_list,
     div_list) = \
        read_file_xlsx(filename_xlsx, growth_rate, priceA_disc, priceB_disc, Nyrs, path_quotes)

    d = {'tgt_price': [], 'price': [], 'perc_to_increase': [], 'year_last_update': [], 'report_release': [],
         'div_yield': []}
    for i in range(len(name_list)):
        d['year_last_update'].append(int(year_last_update_list[i]))
        d['tgt_price'].append(tgt_price_list[i])
        d['price'].append(price_list[i])
        d['perc_to_increase'].append(perc_to_increase_list[i] * 100)
        d['report_release'].append(report_release[i])
        d['div_yield'].append(float(div_list[i]) / float(price_list[i]) * 100)

    df = pd.DataFrame(d, index=name_list)
    df = df.sort_values(by='perc_to_increase', ascending=False)

    # Determine if EPS metrics require updating
    df['is_updated'] = df.apply(lambda row: get_is_updated(row['year_last_update'], row['report_release'], row.name), axis=1)

    print("\n")
    print(tabulate(df[['perc_to_increase', 'price', 'tgt_price', 'year_last_update', 'report_release', 'is_updated',
                       'div_yield']],
                   headers='keys', tablefmt='psql'))