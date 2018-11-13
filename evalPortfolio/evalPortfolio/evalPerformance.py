# Ng Yibin, Jan 2018
# Evaluates the performance of the portfolio across days

import argparse
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import pandas as pd

from tabulate import tabulate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluates the performance of the portfolio across days.')
    parser.add_argument('dir_in', help='Enter the dir of the input files here.')
    args = parser.parse_args()

    df = pd.DataFrame()
    for file in os.listdir(args.dir_in):
        df_temp = pd.read_csv(args.dir_in + "/" + file, sep =",")
        df_temp['date'] = file.split(".")[0]
        df = pd.concat([df, df_temp], axis=0)
    df.index = df['date']

    # Compute daily gain (dollars)
    df['Daily gain'] = df['Total portfolio market value (mark to market)'].diff()

    # Compute daily return (%)
    df['Daily return'] = df['Total portfolio market value (mark to market)'].pct_change()*100.0

    # Compute Sharpe ratio
    df['Sharpe ratio'] = df['Daily return'].expanding().mean() / df['Daily return'].expanding().std()

    df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')
    print(tabulate(df, headers='keys', tablefmt='psql'))

    cols = ['Total portfolio market value (mark to market)',
            'Total profit (mark to market)',
            'Total profit (mark to market) with dividends and drp included']
    df[cols].plot(subplots=True, layout=(3, 1), figsize=(6, 6), sharex=True, style='x-', grid=True)

    # # Plot Total portfolio market value column
    # ax = df.plot(x='date', y='Total portfolio market value (mark to market)', style='x-')
    # ax.set_xlabel("Date")
    # ax.set_ylabel("Total portfolio market value (mark to market)")
    # ax.grid(True)
    # plt.show()
    #
    # # Plot Total profit column
    # ax = df.plot(x='date', y='Total profit (mark to market)', style='x-')
    # ax.set_xlabel("Date")
    # ax.set_ylabel("Total profit (mark to market)")
    # ax.grid(True)
    # plt.show()
    #
    # # Plot Total profit column
    # ax = df.plot(x='date', y='Total profit (mark to market) with dividends and drp included', style='x-')
    # ax.set_xlabel("Date")
    # ax.set_ylabel("Total profit (mark to market) with dividends and drp included")
    # ax.grid(True)
    # plt.show()

    # Plot Daily gain column
    ax = df.plot(x='date', y='Daily gain', style='x-')
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily gain")
    ax.grid(True)
    plt.show()

    # Plot weighted CAGR
    ax = df.plot(x='date', y='Weighted cagr with dividends and drp included', style='x-')
    ax = df.plot(x='date', y='Weighted cagr for benchmark', style='rx-', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Weighted CAGR (%)")
    ax.grid(True)
    plt.show()

