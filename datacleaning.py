import yfinance as yf
import pandas as pd
import math
import numpy as np
import os
# good to check and make sure you are in the right file to access your work!
path = os.getcwd()
files = os.listdir(path)
print(files)
# upload the output of KWP510datacollection.py to begin cleaning and imputing missing values, first data, then index
df_main = pd.read_csv('dataforcleaning.csv')
print(df_main.info())
for column in df_main.columns:
    null_vals = df_main[column].isnull().sum()
    if null_vals > 0:
        print(f'The {column} column has {null_vals} null values')
# this will impute the missing price/earnings ratio values by using a yfinance reference and/or calculation.
# imputed/constructed values will have an additional digit than scraped peers for rapid identification
print('Please wait while missing price earnings ratios are calculated...')
for index, row in df_main.iterrows():
    if math.isnan(row['Price Earnings Ratio']):  # harder than it looks!
        try:
            ticker = yf.Ticker(row['Ticker'])
            ticker_PE = ticker.income_stmt.loc['Diluted EPS'][0]
            if math.isnan(ticker_PE):
                ticker = yf.Ticker(row['Ticker'])
                ticker_ebitda = ticker.income_stmt.loc['EBITDA'][0]
                ticker_shares = ticker.balance_sheet.loc['Share Issued'][0]
                ticker_eps = ticker_ebitda / ticker_shares
                ticker_PE = row['Current Price'] / ticker_eps
                df_main.at[index, 'Price Earnings Ratio'] = round(float(ticker_PE), 3)
            else:
                df_main.at[index, 'Price Earnings Ratio'] = round(float(ticker_PE), 3)
        except:
            ticker = yf.Ticker(row['Ticker'])
            ticker_ebitda = ticker.income_stmt.loc['EBITDA'][0]
            ticker_shares = ticker.balance_sheet.loc['Share Issued'][0]
            ticker_eps = ticker_ebitda / ticker_shares
            ticker_PE = row['Current Price'] / ticker_eps
            df_main.at[index, 'Price Earnings Ratio'] = round(float(ticker_PE), 3)
print('Missing Price Earnings Ratios computed!')
# now with price earnings data complete, we can compute an assessed valuation.
print('Please wait while missing valuations are being assessed...')
# the sector specific price earnings ration will be used for comparison of peers
sector_pe = df_main.groupby('Sector')['Price Earnings Ratio'].mean()
sector_pe_dict = sector_pe.to_dict()
for index, row in df_main.iterrows():
    if pd.isnull(row['Valuation']):
        proximity = abs(row['Price Earnings Ratio'] - sector_pe_dict.get(row['Sector'])
                        / sector_pe_dict.get(row['Sector']))
        if proximity <= .1:  # tickers +/- 10% of their Sector average PE will be rated "Near Fair Value"
            df_main.at[index, 'Valuation'] = 'Near Fair Value'
        elif row['Price Earnings Ratio'] - sector_pe_dict.get(row['Sector']) / sector_pe_dict.get(row['Sector']) > .1:
            df_main.at[index, 'Valuation'] = 'Overvalued'
        else:
            df_main.at[index, 'Valuation'] = 'Undervalued'
print('Missing valuations computed!')
print('Please wait while missing target price is calculated...')
# Calculating a target price is a full time job for a financial analyst, so we'll take some shortcuts!
max_pe = max(df_main['Price Earnings Ratio'])
for index, row in df_main.iterrows():
    if math.isnan(row['Target Price']):
        pe = row['Price Earnings Ratio']
        k = .000001
        dampened_pe = pe / (1 + np.log(np.abs(pe) + k) / max_pe)
        dampened_return = np.sqrt(abs(row['One Year Change']))
        tgt_price = (1 + (dampened_pe * dampened_return / 100)) * row['Current Price']
        df_main.at[index, 'Target Price'] = round(tgt_price, 3)
# this calculation will ensure that companies with negative PE ratios are set a lower target price
# it is assumed that growth/loss in the next year will be much more conservative than last year
print('Missing target prices have been computed!')
print("Please wait while missing Target Proximity's are calculated...")
for index, row in df_main.iterrows():
    if math.isnan(row['Target Proximity']):
        df_main.at[index, 'Target Proximity'] = round(row['Current Price'] / row['Target Price'], 2)
# now we will calculate a buy/sell rating based on mean ratings, by sector, increasing by +1 if 1YC was negative
sector_rating = df_main.groupby('Sector')['Rating'].mean()
sector_rating_dict = sector_rating.to_dict()
for index, row in df_main.iterrows():
    if math.isnan(row['Rating']):
        if row['One Year Change'] > 0:
            df_main.at[index, 'Rating'] = round(sector_rating_dict.get(row['Sector']), 2)
        else:
            df_main.at[index, 'Rating'] = round(sector_rating_dict.get(row['Sector']) + 1, 2)
        # computed ratings will be 2 digits, whereas scraped ones have only 1. Aids in human-readability!
print('Missing ratings have been computed!')
#  now let's calculate market capitalization with our share float information and add as a new column
print(df_main.columns)
df_main['Market Capitalization'] = round(df_main['Current Price'] * df_main['Share Float'], 2)
# quick test to ensure the values of our new column are positive!
for index, row in df_main.iterrows():
    mcv = row['Market Capitalization']
    if mcv < 0:
        print(row['Ticker'])
        raise Exception('Error in Market Capitalization calculation- check current price and share float!')
print(df_main.info())
for column in df_main.columns:
    null_vals = df_main[column].isnull().sum()
    if null_vals > 0:
        print(f'The {column} column has {null_vals} null values')
    else:
        print(f'All missing values in {column} been cleaned!')
df_main.to_csv('dataforanalysis.csv', index=False)
#  now to quickly clean and format our baseline information!
df_indices = pd.read_csv('indexdata.csv')
print(df_indices)
#  the Target Price, Proximity, Rating, and Valuation column are empty, lets drop!
df_indices.drop(['Target Price', 'Target Proximity', 'Rating', 'Valuation'], axis=1, inplace=True)
print(df_indices)
#  the tickers can be hard to read, so let's add back in the Sector names
industry_indexes = {'SPY': 'S&P 500', 'XLC': 'Communication Services', 'XLY': 'Consumer Discretionary',
                    'XLP': 'Consumer Staples', 'XLE': 'Energy', 'XLF': 'Financials', 'XLV': 'Health Care',
                    'XLI': 'Industrials', 'XLB': 'Materials', 'XLRE': 'Real Estate', 'XLK': 'Information Technology'
                    , 'XLU': 'Utilities'}
df_indices['Sector'] = df_indices['Ticker'].map(industry_indexes)
print(df_indices)
#  now lets put things in an order that makes sense for an index
df_indices = df_indices.reindex(columns=['Ticker', 'Sector', 'Avg Volume', 'Current Price', 'Price Earnings Ratio',
                                         'Day Change', 'One Year Change'])
print(df_indices)
#  Perfect!
df_indices.to_csv('indexdataforanalysis.csv', index=False)
print('@'*100)
print('This concludes phase 2 of the project!')
print('Proceed to KWP510dataanalysis.py and follow instructions!')
