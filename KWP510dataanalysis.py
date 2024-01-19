import random
import numpy as np
import pandas as pd
import os
# initialize some tools for later that will ease reading
sadface = '\u2639'
red_start = "\033[91m"
red_end = "\033[0m"
checkmark = '\u2713'
green_start = "\033[92m"
green_end = "\033[0m"
blue_start = "\033[34m"
blue_end = "\033[0m"
# good to check and make sure you are in the right file to access your work!
path = os.getcwd()
files = os.listdir(path)
print(files)
df_main = pd.read_csv('dataforanalysis.csv')
all_stocks_list = df_main['Ticker'].to_list()
print(df_main.head())
portfolio_options = {}  # this is where we will store 1YC of each eventual portfolio option
overvalued = df_main[df_main['Valuation'] == 'Overvalued']
math_overvalued = df_main[df_main['Target Proximity'] > 1][['Ticker', 'Target Proximity']]
undervalued = df_main[df_main['Valuation'] == 'Undervalued']
fair_price = df_main[df_main['Valuation'] == 'Near Fair Value']
fair_price_list = fair_price['Ticker'].to_list()
fair_price_sectors = fair_price['Sector'].value_counts()
fair_price_math = df_main[df_main['Target Proximity'] == 1][['Ticker', 'Target Proximity']]
fair_price_math_list = fair_price_math['Ticker'].to_list()
math_undervalued = df_main[df_main['Target Proximity'] < 1][['Ticker', 'Target Proximity']]
both_over_df = pd.merge(overvalued, math_overvalued, how="inner", on=['Ticker', 'Target Proximity'])  # selections
portfolio_options['Contrarian/Valuation'] = np.mean(both_over_df['One Year Change'])
list_both_over = both_over_df['Ticker'].to_list()
both_over_sectors = both_over_df['Sector'].value_counts()
both_under_df = pd.merge(undervalued, math_undervalued, how='inner', on=['Ticker', 'Target Proximity'])
list_both_under = both_under_df['Ticker'].to_list()
both_under_sectors = both_under_df['Sector'].value_counts()
both_under_lowest_PE_33_max = both_under_df.groupby('Sector').apply(lambda x: x.sort_values(by='Price Earnings Ratio',
                                                                  ascending=False)).reset_index(drop=True)
both_under_lowest_PE_33_max = both_under_lowest_PE_33_max.groupby('Sector').head(3)  # selections
portfolio_options['Traditional/Valuation'] = np.mean(both_under_lowest_PE_33_max['One Year Change'])
list_both_under_lowest_PE_33_max = both_under_lowest_PE_33_max['Ticker'].to_list()
under_over_df = pd.merge(undervalued, math_overvalued, how='inner', on=['Ticker', 'Target Proximity'])
under_over_list = under_over_df['Ticker'].to_list()
over_under_df = pd.merge(overvalued, math_undervalued, how='inner', on=['Ticker', 'Target Proximity'])
over_under_list = over_under_df['Ticker'].to_list()
over_at_fpmath = pd.merge(overvalued, fair_price_math, how='inner', on=['Ticker', 'Target Proximity'])
over_at_fpmath_list = over_at_fpmath['Ticker'].to_list()
under_at_fpmath = pd.merge(undervalued, fair_price_math, how='inner', on=['Ticker', 'Target Proximity'])
under_at_fpmath_list = under_at_fpmath['Ticker'].to_list()
fair_over = pd.merge(fair_price, math_overvalued, how='inner', on=['Ticker', 'Target Proximity'])
fair_over_list = fair_over['Ticker'].to_list()
fair_under = pd.merge(fair_price, math_undervalued, how='inner', on=['Ticker', 'Target Proximity'])
fair_under_list = fair_under['Ticker'].to_list()
fair_and_fair = pd.merge(fair_price, fair_price_math, how='inner', on=['Ticker', 'Target Proximity'])
fair_and_fair_list = fair_and_fair['Ticker'].to_list()
print(f'The number of companies that are labeled as over/undervalued: {len(overvalued) + len(undervalued)}')

print('The number labeled overvalued is:', len(overvalued))
print('The number above their 1YR target price is:', len(math_overvalued))
print('The number above 1YR Target and labeled overvalued is: ', len(list_both_over))
print(f'The tickers of the companies that are overvalued are: {list_both_over}')
print(f'The {len(both_over_sectors)} sectors represented by companies that are over/over and their frequency are: '
      f'\n{both_over_sectors}')
print('_' * 100)

print('The number labeled undervalued is:', len(undervalued))
print('The number below their 1YR target price is:', len(math_undervalued))
print('The number below 1YR Target and labeled undervalued is: ', len(list_both_under))
print(f'The tickers of the companies that are undervalued are: {list_both_under}')
print(f'The {len(both_under_sectors)} sectors represented by companies that are under/under and their frequency are: '
      f'\n{both_under_sectors}')
print(f'Trimming this list down to the top 3 in each Sector, by lowest PE ratio, we now have a collection of '
      f'{len(both_under_lowest_PE_33_max)} stocks')
print(both_under_lowest_PE_33_max)
print('_' * 100)

print('There are also some anomalies that fall into mismatched groups...')
print('The number labeled undervalued and over 1YR Target is: ', len(under_over_list))
print(f'The tickers of the companies that are undervalued are: {under_over_list}')
print('The number labeled overvalued and under 1YR Target is: ', len(over_under_list))
print(f'The tickers of the companies that are undervalued are: {over_under_list}')
print('_' * 100)

print(f'The number of companies that are labelled as "Near Fair Price" is: {len(fair_price_list)}')
print(f'The {len(fair_price_sectors)} sectors represented by companies that are NFP and their frequency are: '
      f'\n{fair_price_sectors}')
print('The number labeled "Near Fair Price" and under 1YR Target is: ', len(fair_under_list))
print(f'The tickers of the companies that are NFP and under 1YR Target are: {fair_under_list}')
print('The number labeled "Near Fair Price" and over 1YR Target is: ', len(fair_over_list))
print(f'The tickers of the companies that are NFP and over 1YR Target are: {fair_over_list}')
print('The number labeled "Near Fair Price" and precisely at 1YR Target is: ', len(fair_and_fair_list))
print(f'The tickers of the companies that are NFP and precisely at 1YR Target are: {fair_and_fair_list}')
print('_' * 100)
print('Thus far it appears that using these two metrics we can begin to rank the stocks, but lets go deeper!')
print('Low Rating (BUY) should correlate with and Undervalued label, but how strong is it?')
under_buy_rating = round(undervalued['Rating'].mean(), 2)
print(f'The average buy/sell rating for "Undervalued" companies is: {under_buy_rating}')
print('We would expect to see a slightly higher rating for "Near Fair Value"')
nfv_buy_rating = round(fair_price['Rating'].mean(), 2)
print(f'The average buy/sell rating for "Near Fair Value" companies is: {nfv_buy_rating}')
over_buy_rating = round(overvalued['Rating'].mean(), 2)
print('And the highest ratings, trending towards SELL, should be labeled "Overvalued"')
print(f'The average buy/sell rating for "Overvalued" companies is: {over_buy_rating}')
print('The buy ratings do not move in a linear fashion along with the valuation rating- this is unexpected!')
print('Perhaps there is another correlation that is more reliable such as the Ratings and the Target Proximity?')
print('_' * 100)
# How well do the buy ratings and target proximity correlate? LET'S FIND OUT
# LOWER price target percentage should correlate with a LOWER buy rating (POSITIVE CORRELATION)
pt_to_rating_corr = round(np.corrcoef(df_main['Target Proximity'], df_main['Rating'])[0, 1], 3)
print(f'The Target Proximity to Buy/Sell Rating correlation coefficient is: {pt_to_rating_corr}')
print('Is the correlation any stronger/weaker when we subset by Valuation?')
print('_' * 100)
pt_to_rating_corr_unders = round(np.corrcoef(undervalued['Target Proximity'], undervalued['Rating'])[0, 1], 3)
pt_to_rating_corr_nfv = round(np.corrcoef(fair_price['Target Proximity'], fair_price['Rating'])[0, 1], 3)
pt_to_rating_corr_overs = round(np.corrcoef(overvalued['Target Proximity'], overvalued['Rating'])[0, 1], 3)
print(f'The Target Proximity to Buy/Sell Rating correlation coefficient for "Undervalued" companies is: '
      f'{pt_to_rating_corr_unders}')
print(f'The Target Proximity to Buy/Sell Rating correlation coefficient for "Near Fair Value" companies is: '
      f'{pt_to_rating_corr_nfv}')
print(f'The Target Proximity to Buy/Sell Rating correlation coefficient for "Overvalued" companies is: '
      f'{pt_to_rating_corr_overs}')
print(f'{red_start}{sadface*10}{red_end} It appears that the coefficient weakens drastically when applied to '
      f'"Overvalued" companies!')
print('_' * 100)
print('Now for the good stuff: how well did these companies perform in the last year?')
print('First, what did returns look like last year?')
_1yc_summary = df_main['One Year Change'].describe()
print(_1yc_summary)
print('What was the standard deviation? Were returns tightly grouped or was there a wide variety?')
print(round(np.std(df_main['One Year Change']), 2), '\b%')
print('It looks like returns were quite varied!')
print('It appears that the last year has been challenging for the S&P 500- the average company lost 7.3%!')
print('\tHowever, due to the weighting of companies in the S&P 500, the 1YC in the index is actually +12.3% '
      'Check ticker: SPY')
under_1yc = round(undervalued['One Year Change'].mean(), 2)
print(f'The average One Year Change for "Undervalued" companies is: {under_1yc}')
nfv_1yc = round(fair_price['One Year Change'].mean(), 2)
print(f'The average One Year Change for "Near Fair Value" companies is: {nfv_1yc}')
over_1yc = round(overvalued['One Year Change'].mean(), 2)
print(f'The average One Year Change for "Overvalued" companies is: {over_1yc}')
print(f'{green_start}{checkmark*10}{green_end} It appears that companies that did well/poorly in the last year tend to'
      f' be Overvalued/Undervalued')
print('Do the Analyst Ratings correlate with annual return? Low rating is preferred so the correlation should be '
      'negative if the ratings are meaningful')
rating_to_1yc = round(np.corrcoef(df_main['Rating'], df_main['One Year Change'])[0, 1], 3)
print(rating_to_1yc)
print(f'{green_start}{checkmark*10}{green_end} It looks like the Analysts are rating strong performing companies '
      f'fairly well!')
#rating portion
df_rating_by_sector = df_main.groupby('Sector').apply(lambda x: x.sort_values(by='Rating',
                                                                  ascending=True)).reset_index(drop=True)
df_rating_top_3_by_sector = df_rating_by_sector.groupby('Sector').head(3)  # selections
portfolio_options['Traditional/Rating'] = np.mean(df_rating_top_3_by_sector['One Year Change'])
list_df_rating_top_3_by_sector = df_rating_top_3_by_sector['Ticker'].to_list()
print('With that in mind, lets take a look at the top three rated Companies of last year, by Sector')
print(df_rating_top_3_by_sector)
df_rating_bottom_3_by_sector = df_rating_by_sector.groupby('Sector').tail(3)  # selections
portfolio_options['Contrarian/Rating'] = np.mean(df_rating_bottom_3_by_sector['One Year Change'])
list_df_rating_bottom_3_by_sector = df_rating_bottom_3_by_sector['Ticker'].to_list()
print('Now lets see the three worst rated, by Sector')
print(df_rating_bottom_3_by_sector)
print('_' * 100)
print('Now we will analyze Volume- what was the average number of shares traded per company?')
print(df_main['Avg Volume'].describe())
print('What was the standard deviation? Does each company receive the same amount of attention?')
print(round(np.std(df_main['Avg Volume']), 2), '\b%')
print('WOW! The standard deviation is 3x the average stock- this is a diverse market!')
print('More volume means a more popular stock. Did these ones do well last year?')
avg_vol_to_1yc = round(np.corrcoef(df_main['Avg Volume'], df_main['One Year Change'])[0, 1], 3)
print(avg_vol_to_1yc)
print(f'{red_start}{sadface*10}{red_end}There is no significant correlation there. Even unpopular stocks can do well!')
avg_vol_to_cp = round(np.corrcoef(df_main['Avg Volume'], df_main['Current Price'])[0, 1], 3)
print(avg_vol_to_cp)
print('The effect is slight, but an inverse correlation demonstrates that lower priced stocks have more volume.')
print('What about Volume vs Price Earnings? Perhaps companies with lower PE receive more volume? (Negative CORR)')
avg_vol_to_pe = round(np.corrcoef(df_main['Avg Volume'], df_main['Price Earnings Ratio'])[0, 1], 3)
print(avg_vol_to_pe)
print(f'{red_start}{sadface*10}{red_end}There is almost no correlation between volume and PE ratio!')
print('The top 3 most traded companies, by sector, are:')
volume_by_sector = df_main.groupby('Sector').apply(lambda x: x.sort_values(by='Avg Volume',
                                                                  ascending=False)).reset_index(drop=True)
top_volume_by_sector = volume_by_sector.groupby('Sector').head(3)  # selections
portfolio_options['Traditional/Volume'] = np.mean(top_volume_by_sector['One Year Change'])
list_top_volume_by_sector = top_volume_by_sector['Ticker'].to_list()
bottom_volume_by_sector = volume_by_sector.groupby('Sector').tail(3)  # selections
portfolio_options['Contrarian/Volume'] = np.mean(bottom_volume_by_sector['One Year Change'])
list_bottom_volume_by_sector = bottom_volume_by_sector['Ticker'].to_list()
print(top_volume_by_sector)
print('And the least traded companies are:')
print(bottom_volume_by_sector)
print('_' * 100)
print('What about the price of stocks? Perhaps cheaper ones appeal more to the masses and did well last year?')
cp_to_1yc = round(np.corrcoef(df_main['Current Price'], df_main['One Year Change'])[0, 1], 3)
print(cp_to_1yc)
print(f'{green_start}{checkmark*10}{green_end}A .28 correlation between Current Price and 1YC moderately suggests '
      f'that pricier stocks did better!')
print("Are stocks trending in the same direction as their 1YC or are they going in a new direction?")
dc_to_1yc = round(np.corrcoef(df_main['Day Change'], df_main['One Year Change'])[0, 1], 3)
print(dc_to_1yc)
print(f"{green_start}{checkmark*10}{green_end}There is an observed connection between last years performance and "
      f"today's, suggesting a stable market!")
print('Are PE correlated with 1YC? A strong positive ratio would imply that earnings are not keeping up, '
      'suggesting overvalued')
pe_to_1yc = round(np.corrcoef(df_main['Price Earnings Ratio'], df_main['One Year Change'])[0, 1], 3)
print(pe_to_1yc)
print(f'{green_start}{checkmark*10}{green_end}As expected, there is an observed correlation between higher PE ratio '
      f'and 1YC, suggesting that companies that did well last year have not seen the underlying earnings '
      f'increases materialize yet, implying current overvaluation.')
print('If the market was, at large, overvalued, we would expect that higher priced stocks would also have higher PE')
cp_to_pe = round(np.corrcoef(df_main['Current Price'], df_main['Price Earnings Ratio'])[0, 1], 3)
print(cp_to_pe)
print(f'{red_start}{sadface*10}{red_end} This does not seem to be the case, there are still good deals in the market!')
print('_' * 100)
print("Let's look deeper to find if those deals might be sector specific, lets start with PE to 1YC")
pe_to_1yc_sectors = df_main.groupby('Sector').apply(lambda x: np.corrcoef(x['Price Earnings Ratio'],
                                                                          x['One Year Change'])[0, 1]).reset_index()
pe_to_1yc_sectors.columns = ['Sector', 'PE to 1YC Corr']
pe_to_1yc_sectors['PE to 1YC Rank'] = pe_to_1yc_sectors['PE to 1YC Corr'].rank(ascending=True).astype(int)
print(pe_to_1yc_sectors.sort_values(by='PE to 1YC Corr'))
print('This table shows us the relatively better valued sectors on top. Consumer Staples being the best deal and '
      'Information Technology being the most overvalued')
print('Perhaps there is some merit to Information Technology being overpriced? What were returns last year, by Sector?')
_1yc_by_sector = df_main.groupby('Sector')['One Year Change'].mean().reset_index()
_1yc_by_sector.columns = ['Sector', 'One Year Change']
_1yc_by_sector['1YC Rank'] = _1yc_by_sector['One Year Change'].rank(ascending=False).astype(int)
print(_1yc_by_sector.sort_values(by='One Year Change', ascending=False))
print('Perhaps the sector index funds fared any better? Is there any benefit in buying individually?')
df_index = pd.read_csv('indexdataforanalysis.csv')
portfolio_options['S&P 500'] = df_index['One Year Change'][0]
print(df_index.sort_values('One Year Change', ascending=False))
print('These funds, due to weighting their constituents correctly, far outperformed a blanket allocation across the'
      'sectors, represented by the mean performance figures in our previous table!')  # useful for selection!
print('This is the same effect as was observed on the index at whole previously, that is, an even allocation across'
      'all 503 companies last year would have lost 7%, whereas a properly weighted allocation across would have '
      'gained 12%- an enormous margin of difference!')
positive_sectors_1yc = []
negative_sectors_1yc = []
for index, row in _1yc_by_sector.iterrows():
    if row['One Year Change'] >= 0:
        positive_sectors_1yc.append(row['Sector'])
    else:
        negative_sectors_1yc.append(row['Sector'])
print(f'These sectors had positive returns last year: {positive_sectors_1yc}')
print(f'These sectors had negative returns last year: {negative_sectors_1yc}')
print('This information will come in handy for stock selection, depending on customer risk profile!')
print('_' * 100)
print('What were the best performing companies last year, by sector? And what was their combined average return?')
df_top_of_sectors = df_main.groupby('Sector').apply(lambda x: x.sort_values(by='One Year Change',
                                                                  ascending=False)).reset_index(drop=True)
df_top_3_of_sectors = df_top_of_sectors.groupby('Sector').head(3)
list_df_top_3_of_sectors = df_top_3_of_sectors['Ticker'].to_list()  # these will be useful for selection
portfolio_options['Traditional/Historical Return'] = np.mean(df_top_3_of_sectors['One Year Change'])
df_bottom_3_of_sectors = df_top_of_sectors.groupby('Sector').tail(3)
list_df_bottom_3_of_sectors = df_bottom_3_of_sectors['Ticker'].to_list()  # these will be useful for selection
portfolio_options['Contrarian/Historical Return'] = np.mean(df_bottom_3_of_sectors['One Year Change'])
top_3_of_sector_return = df_top_3_of_sectors['One Year Change'].mean()
bottom_3_of_sector_return = df_bottom_3_of_sectors['One Year Change'].mean()
print(df_top_3_of_sectors)
print(f'A portfolio of the three best performers in each sector last year would have netted '
      f'{green_start}{top_3_of_sector_return}{green_end}')
print('Conversely, which were the worst of their sector? And what was their combined average return?')
print(df_bottom_3_of_sectors)
print(f'A portfolio of the bottom three performers in each sector last year would have netted {red_start}'
      f'{bottom_3_of_sector_return}{red_end}')
print('Pretty astounding/disappointing results on either side, but important to note that the best returned almost'
      ' 7% more than the worst lost, resulting in a overall gain if one were to diversify across both groups! '
      'Of greater significant, the best five of sector more than doubled the average return of the market, implying an'
      'opportunity for concentration, if one were to anticipate the next year to be the same as last (doubtful!)')
print('_' * 100)
print("Let's pivot to another important factor: Market Capitalization- where is the money in the market?")
sp500_mc_by_sector = df_main.groupby('Sector')['Market Capitalization'].sum().reset_index()
sp500_mc_by_sector.columns = ['Sector', 'Market Capitalization']
sp500_mc_by_sector = sp500_mc_by_sector.sort_values(by='Market Capitalization', ascending=False)
sp500_total_mc = sp500_mc_by_sector['Market Capitalization'].sum()
sp500_mc_by_sector['% of S&P 500'] = sp500_mc_by_sector['Market Capitalization'] / sp500_total_mc
print(sp500_mc_by_sector)
print('Brilliant! The S&P 500 is heavily composed of Information Tech and Financial Companies')
print('What are the top three companies in each Sector? How much do these companies contribute to the index?')
df_mcbs = df_main.groupby('Sector').apply(lambda x: x.sort_values(by='Market Capitalization',
                                                                  ascending=False)).reset_index(drop=True)
df_mcbs['% of S&P 500'] = round(df_mcbs['Market Capitalization'] / sp500_total_mc, 5)
df_mcbs_top3 = df_mcbs.groupby('Sector').head(3)  # selections
portfolio_options['Traditional/Market Cap'] = np.mean(df_mcbs_top3['One Year Change'])
df_mcbs_bottom3 = df_mcbs.groupby('Sector').tail(3)  # selections
portfolio_options['Contrarian/Market Cap'] = np.mean(df_mcbs_bottom3['One Year Change'])
list_df_mcbs_bottom3 = df_mcbs_bottom3['Ticker'].to_list()
df_mcbs_top3_filtered = df_mcbs_top3.loc[:, ['Ticker', 'Current Price', 'Sector', 'Market Capitalization',
                                             '% of S&P 500']]
list_df_mcbs_top3_filtered = df_mcbs_top3_filtered['Ticker'].to_list()
print(df_mcbs_top3_filtered)
df_mcbs_top3_sum = df_mcbs_top3['Market Capitalization'].sum()
print(f'Their combined contribution to the total market cap of the index is: {df_mcbs_top3_sum}')
print('Conversely, what about the smallest three market cap companies, by Sector- how much do they contribute?')
df_mcbs_bottom3_filtered = df_mcbs_bottom3.loc[:, ['Ticker', 'Current Price', 'Sector', 'Market Capitalization',
                                                   '% of S&P 500']]
print(df_mcbs_bottom3_filtered)
df_mcbs_bottom3_sum = df_mcbs_bottom3['Market Capitalization'].sum()
print(f'Their combined contribution to the total market cap of the index is: {df_mcbs_bottom3_sum}')
mc_weight_imbalance = df_mcbs_top3_sum / df_mcbs_bottom3_sum
print(f'272 Billion versus 16.6 Trillion means most of the market value is concentrated in those large companies, by a '
      f'factor of {round(mc_weight_imbalance, 2)} times!')
# print(df_mcbs) # all companies with their weighting of the index, useful for selection

max_mc = df_mcbs['% of S&P 500'].max()
max_mc_ticker = df_mcbs.loc[df_mcbs['% of S&P 500'] == max_mc, 'Ticker'].iloc[0]
min_mc = df_mcbs['% of S&P 500'].min()  # small percentage so let's reformat to make it readable
min_mc_dec = '{:.5f}'.format(min_mc)
min_mc_ticker = df_mcbs.loc[df_mcbs['% of S&P 500'] == min_mc, 'Ticker'].iloc[0]
print(f'The smallest contributor to the index market share is {min_mc_ticker}:{min_mc_dec} and the largest is '
      f'{max_mc_ticker}:{max_mc}')
print('The money in the S&P500 is heavily concentrated in the largest market cap companies, but did they outperform?')
mc_to_1yc = round(np.corrcoef(df_main['Market Capitalization'], df_main['One Year Change'])[0, 1], 3)
print(f'The correlation between Market Cap and 1YC is {mc_to_1yc}!')
print(f'{green_start}{checkmark*10}{green_end}It does appear that the larger a company is, the better it performed!')
print(f'{green_start} Given the information we have seen we can now build some portfolio models and start investing'
      f' wisely! {green_end}')
print('_' * 100)
print('_' * 100)
print('_' * 100)
print('As a brief summary, we have calculated that market cap, current price, sector, and rating all have observed'
      'historical correlations \nthat can be taken into the formation of an investment strategy. However, as current '
      'price is the most easily manipulated through a \nsplit/reverse spit, it would be more sound to drop this option'
      ' and use market cap instead, as it is a function of the price.')
print('We will ask the customer to answer a few quick questions about their preferences in order to aid in the '
      'selection of their stocks!')
traditional_lists = [list_df_top_3_of_sectors, list_both_over, list_df_mcbs_top3_filtered, list_top_volume_by_sector,
                     list_df_rating_top_3_by_sector]
contrarian_lists = [list_df_bottom_3_of_sectors, list_both_under_lowest_PE_33_max, list_df_mcbs_bottom3,
                    list_bottom_volume_by_sector, list_df_rating_bottom_3_by_sector]
question1 = input('Are you a traditional or contrarian investor? Please enter "traditional" or "contrarian".')
if question1.lower() == 'traditional':
    list_set = traditional_lists
elif question1.lower() == 'contrarian':
    list_set = contrarian_lists
else:
    raise Exception('Invalid input. Please enter either: "traditional" or "contrarian"')
question2 = input('What metric is most important to you? Select from "Historical Return", "Valuation", "Market Cap",'
                  ' "Volume", "Rating", or "NOT SURE"') # not sure returns a random selection
if question2.lower() == 'historical return':
    selections = list_set[0]
    my_portfolio = df_main[df_main['Ticker'].isin(selections)]
elif question2.lower() == 'valuation':
    selections = list_set[1]
    my_portfolio = df_main[df_main['Ticker'].isin(selections)]
elif question2.lower() == 'market cap':
    selections = list_set[2]
    my_portfolio = df_main[df_main['Ticker'].isin(selections)]
elif question2.lower() == 'volume':
    selections = list_set[3]
    my_portfolio = df_main[df_main['Ticker'].isin(selections)]
elif question2.lower() == 'rating':
    selections = list_set[4]
    my_portfolio = df_main[df_main['Ticker'].isin(selections)]
elif question2.lower() == 'not sure':
    selections = random.sample(all_stocks_list, 30)
    my_portfolio = df_main[df_main['Ticker'].isin(selections)]
else:
    raise Exception('Please select from one of the specified options')
print(f'Based on your input, your stock selections are the following: {selections}')
capital = input('How much would you like to invest? Please a positive integer value greater than 30000, e.g. "1000000"')
try:
    capital = int(capital)
    if capital < 30000:
        raise Exception("Starting capital must be at least 30000- it takes money to make money!")
except:
    raise Exception('Invested capital must only be numbers, no commas or other punctuation')
if capital < 0:
    raise Exception('You cannot invest negative money- no short selling allowed here!')
allocation_amount = capital / len(selections)
for index, row in df_main.iterrows():
    if row['Ticker'] in selections:
        stock = row['Ticker']
        cp = row['Current Price']
        if cp > allocation_amount:
            raise Exception('Insufficient funds to execute this strategy. Raise more capital and return then!')
        share_count = allocation_amount // cp
        capital_spent = round(share_count * cp, 2)
        capital = round(capital - capital_spent, 2)
        print(f'Buy {blue_start}{share_count} shares of {stock}{blue_end} for {green_start}{capital_spent}{green_end}.'
              f' You have ${green_start}{capital}{green_end} remaining')
print(f'You have {green_start}${capital}{green_end} left over for emergencies.')
#print(my_portfolio)
print('#'*100)
df_main.to_csv('dataforvisualization.csv', index=False)
sp500_mc_by_sector.to_csv('dataforvisualization1.csv', index=False)
portfolio_options_df = pd.DataFrame.from_dict(portfolio_options, orient='index',
                                              columns=['One Year Change'])
portfolio_options_df.index.names = ['Strategy']
portfolio_options_df.to_csv('portfolio_options_performance.csv')
my_portfolio.to_csv('myportfolio.csv', index=False)
print('This concludes phase 3 of the project!')
print('Proceed to KWP510datavisualization.py and follow instructions!')
