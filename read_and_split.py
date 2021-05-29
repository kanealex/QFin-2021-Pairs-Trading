# -*- coding: utf-8 -*-
"""
    read_and_split
    ~~~~~~~~~~~~~~
    Based on Financials.csv read Ticker then find matched files and merge

    Log:
    20210513
"""

__version__ = '0.1'

import pandas as pd


def read_and_merge(
        financials_file_path='./SectorTickers/Financials.csv',
        csv_base_path='ticker_breakdown',
        save_name='mergedata.csv'
):
    """
        read and merge
    :param financials_file_path: Financials.csv save location
    :param csv_base_path:   csv file save path
    :param save_name:   Output save file name
    :return:
    """

    time_dict = {}
    stocks = []
    for stock_name in pd.read_csv(financials_file_path).Ticker.to_list():
        try:
            file_path = f"{csv_base_path}/{stock_name}.csv"
            print(f"download {file_path} file..", end='')
            df = pd.read_csv(file_path, names=['time_tick', 'price'], dtype={'time_tick': str})
            stocks.append(stock_name)
            for ind, row in df.iterrows():
                if not time_dict.__contains__(row.time_tick):
                    time_dict[row.time_tick] = {}
                time_dict[row.time_tick][stock_name] = row.price
            print('Done')
        except Exception as e:
            print(f"fail！！！ {e}")

    data_lists = []
    for tk, v in time_dict.items():
        row = [tk] + [v[stock] for stock in stocks]
        data_lists.append(row)
    print('merging...', end='')
    pd.DataFrame(data_lists, columns=['time_tick'] + stocks).to_csv(save_name)
    print('Finish!')


if __name__ == '__main__':
    read_and_merge()

