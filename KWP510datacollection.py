import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import yfinance as yf
#  test_list = ['AAPL', 'MSFT', 'GOOG', 'NVDA', 'ANET', 'HD', 'MCD']


def get_sp500_tickers() -> pd.DataFrame:
    """Parse Wikipedia with BeautifulSoup for S&P500 companies for current listing and return their associated 'ticker'.
    The ticker is the common financial shorthand that is associated with each stock listing and will be used throughout
    as the key in several dictionaries created for these companies. There is a condition that will return a
    historical list of the member companies, if the website fails."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    tickers = []  # 0 index from table
    sectors = []  # 2 index from table
    date_added = []  # 5 index from table
    ciks = []  # 6 index from table
    col_headers = ['Ticker', 'Sector', 'Date Added', 'CIK']
    if response.status_code != 200:
        tickers = ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADM', 'ADBE', 'ADP', 'AES', 'AFL', 'A', 'ABNB', 'APD', 'AKAM',
                   'ALK', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AMD',
                   'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON',
                   'APA', 'AAPL', 'AMAT', 'APTV', 'ACGL', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'AZO', 'AVB', 'AVY',
                   'AXON', 'BKR', 'BALL', 'BAC', 'BBWI', 'BAX', 'BDX', 'WRB', 'BRK.B', 'BBY', 'BIO', 'TECH', 'BIIB',
                   'BLK', 'BX', 'BK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'BG',
                   'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE',
                   'CBRE', 'CDW', 'CE', 'COR', 'CNC', 'CNP', 'CDAY', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB',
                   'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA',
                   'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CTVA', 'CSGP', 'COST', 'CTRA', 'CCI',
                   'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR',
                   'DFS', 'DIS', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DTE', 'DUK', 'DD', 'EMN', 'ETN', 'EBAY',
                   'ECL', 'EIX', 'EW', 'EA', 'ELV', 'LLY', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX',
                   'EQR', 'ESS', 'EL', 'ETSY', 'EG', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS',
                   'FICO', 'FAST', 'FRT', 'FDX', 'FITB', 'FSLR', 'FE', 'FIS', 'FI', 'FLT', 'FMC', 'F', 'FTNT', 'FTV',
                   'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT', 'GEHC', 'GEN', 'GNRC', 'GD', 'GE', 'GIS', 'GM', 'GPC',
                   'GILD', 'GL', 'GPN', 'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT',
                   'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUBB', 'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX',
                   'ITW', 'ILMN', 'INCY', 'IR', 'PODD', 'INTC', 'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ',
                   'INVH', 'IQV', 'IRM', 'JBHT', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KVUE', 'KDP', 'KEY',
                   'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN',
                   'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LULU', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC',
                   'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP',
                   'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI',
                   'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS',
                   'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'ON', 'OKE',
                   'ORCL', 'OTIS', 'PCAR', 'PKG', 'PANW', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PEP', 'PFE',
                   'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU',
                   'PEG', 'PTC', 'PSA', 'PHM', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN',
                   'RF', 'RSG', 'RMD', 'RVTY', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB',
                   'STX', 'SEE', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SNA', 'SEDG', 'SO', 'LUV', 'SWK', 'SBUX',
                   'STT', 'STLD', 'STE', 'SYK', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TRGP', 'TGT',
                   'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB',
                   'TFC', 'TYL', 'TSN', 'USB', 'UDR', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR',
                   'VLTO', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VTRS', 'VICI', 'V', 'VMC', 'WAB', 'WBA', 'WMT', 'WBD',
                   'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WRK', 'WY', 'WHR', 'WMB', 'WTW', 'GWW', 'WYNN',
                   'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable sortable"})
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text.strip()
        tickers.append(ticker)  # this creates the list of current S&P500 companies
        sector = row.findAll("td")[2].text.strip()
        sectors.append(sector)  # creates list of their sector
        join_date = row.findAll("td")[5].text.strip('?')
        date_added.append(join_date)  # creates list of their dates when added to the index
        cik = row.findAll("td")[6].text.strip()  # central index key for SEC filings (financial statements)
        ciks.append(cik)  # creates list of their CIK (unique values)
    stock_df = pd.DataFrame([tickers, sectors, date_added, ciks]).T  # .T will transpose list vertical
    stock_df.columns = col_headers  # set our header names
    return stock_df


def get_stock_data(ticker: str) -> list:
    """This function will input a string that must be an actively traded 'ticker' on a US-based stock exchange. It will
    seek to return eight associated values that will be used for future analysis and comparison. Scraped values are
    formatted upon retrieval to streamline data cleaning. Values that are not available will be left as null values
    to be address in the cleaning stage.

    Returns:
    1) cp_float: the current trading price of the stock (float)
    2) day_change_pct: the percentage change in price of the stock (float)
    3) pt_float: the 1-year analyst projected price target (float)
    4) proximity_to_target: calculated percentage of the current price vs. target price (float)
    5) avg_vol: the average amount of shares of the stock that are traded each day (integer)
    6) pe_float: the current price/earning ration of the stock (float)
    7) rtg_float: the average analyst buy/sell rating, 1-6 scale where 1 = BUY <-> 5 = SELL (float)
    8) valuation: the average analyst valuation assessment: Under/Fair/Over-valued (string)
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", }  # causes error on analyst recommendation
    try:
        html = requests.get(f"https://finance.yahoo.com/quote/{ticker}", headers=headers, timeout=10)
    except:
        raise Exception('Unable to access yahoo finance website.')
    try:
        soup = BeautifulSoup(html.text, "html.parser")
    except:
        raise Exception('Unable to parse your HTML request.')
    #  1/8 outputs
    try:
        cur_price = soup.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text
        cur_price_100x = cur_price.replace('.', '').replace(',', '')
        cp_float = float(cur_price_100x) / 100
    except:
        raise Exception('Unable to find current price for your ticker.')
    try:
        summary_info = soup.find_all(class_='Ta(end) Fw(600) Lh(14px)')
    except:
        raise Exception('Unable to find summary information for your ticker.')
    #  2/8 outputs
    try:
        pe_ratio = summary_info[10].text
        pe_float = float(pe_ratio)
    except:
        pe_float = ''
    #  3/8 outputs
    try:
        price_target = summary_info[15].text
        pt_float = price_target.replace('.', '').replace(',', '')
        pt_float_100x = float(pt_float)
        pt_float = pt_float_100x / 100
    except:
        pt_float = ''
    #  4/8 outputs
    try:
        open_price = summary_info[1].text
        open_price_100x = open_price.replace('.', '').replace(',', '')
        open_float = float(open_price_100x) / 100
        day_change_pct = round((cp_float - open_float) / open_float * 100, 2)
    except:
        raise Exception('Unable to find opening price for your ticker.')
    #  5/8 outputs
    try:
        avg_vol = summary_info[7].text
        avg_vol_100x = avg_vol.replace('.', '').replace(',', '')
        avg_vol = int(avg_vol_100x)
    except:
        avg_vol = ''
    #  6/8 outputs
    try:
        proximity_to_target = round((cp_float / pt_float), 2)
    except:
        proximity_to_target = ''
    #  7/8 outputs
    try:
        html = requests.get(f"https://finance.yahoo.com/quote/{ticker}")  # call again without headers, avoids issue
        soup = BeautifulSoup(html.text, "html.parser")
        rating = soup.find("div", {"data-test": "rec-rating-txt"}).text.split(";")[-1].strip()
        rating_flt = float(rating.replace("'", ''))
    except:
        rating_flt = ''
    # 8/8 outputs
    try:
        valuation = soup.find('div', class_="Fw(b) Fl(end)--m Fz(s) C($primaryColor)").text
    except:
        valuation = ''
    #  current price & day change percent kept on the left (priority information)
    return [cp_float, day_change_pct, pt_float, proximity_to_target, avg_vol, pe_float, rating_flt, valuation]


def get_price_data(ticker: str):
    """Unused, retain as backup/further analysis"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", }
    html = requests.get(f"https://finance.yahoo.com/quote/{ticker}/key-statistics", headers=headers)
    soup = BeautifulSoup(html.text, "lxml")
    price_info = soup.find_all(class_='Fw(500) Ta(end) Pstart(10px) Miw(60px)')
    _52_wk_chg = float(price_info[1].text.replace('%', '').replace('.', '')) / 100
    _52_wk_sp500_chg = float(price_info[2].text.replace('%', '').replace('.', '')) / 100
    alpha = round(_52_wk_chg - _52_wk_sp500_chg, 2)
    # ttm_high = float(price_info[3].text.replace('%', '').replace('.', '')) / 100
    # ttm_low = float(price_info[4].text.replace('%', '').replace('.', '')) / 100
    revenue = price_info[35].text
    if revenue.endswith('B'):
        revenue = revenue.replace('B', '0000000').replace('.', '')
        revenue = int(revenue)
    elif revenue.endswith('M'):
        revenue = revenue.replace('M', '0000').replace('.', '')
        revenue = int(revenue)
    return [alpha, revenue]


def split_to_sector(df: pd.DataFrame, sector: str) -> list:
    """Unused, might be useful for visualization stage"""
    tickers = []
    for index, row in df.iterrows():
        if row['Sector'] == sector:
            tickers.append(row['Ticker'])
    return tickers


def one_year_change(ticker: str) -> float:
    """This function will input a stock ticker string and, using the yfinance package, return the percent change in the
    price of the stock over the last year (float)"""
    try:
        ticker_init = yf.Ticker(ticker.replace('.', '-'))
        one_year_ago = (dt.datetime.now() - dt.timedelta(days=365)).strftime('%Y-%m-%d')
        ticker_1yc = ticker_init.history(start=one_year_ago, end=dt.datetime.now().strftime('%Y-%m-%d'))
        ticker_1yc_percent = (ticker_1yc['Close'][-1] - ticker_1yc['Close'][0]) / ticker_1yc['Close'][0] * 100
        print(ticker_1yc_percent)
    except:
        ticker_1yc_percent = ''
    return ticker_1yc_percent


def share_float(ticker: str) -> float:
    """This function will input a stock ticker string and, using the yfinance package, return the number of publicly
     available shares currently available in the market, called the "public float". This share count is used
      to calculate the total Market Capitalization of the stock, as Price x Share Count = Market Share (integer)"""
    try:
        float_init = yf.Ticker(ticker.replace('.', '-'))
        float_return = float_init.get_shares_full()[0]
        print(float_return)
    except:
        float_return = ''
    return float_return


# Call the functions and begin to compile the data
tables_sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df1 = tables_sp500[0]  # this will provide us the current index member tickers to begin scraping their data
stocks_and_data = []
for ticker in df1['Symbol']:    # use test_list to test and df1['Symbol'] for the real deal
    stock_data = get_stock_data(ticker.replace('.', '-'))
    stock_data.insert(0, ticker)
    stocks_and_data.append(stock_data)
    print(stock_data)

df2 = pd.DataFrame(stocks_and_data, columns=['Ticker', 'Current Price', 'Day Change', "Target Price",
                                             "Target Proximity", 'Avg Volume', 'Price Earnings Ratio', 'Rating',
                                             'Valuation'])
sp500 = get_sp500_tickers()
sp500merged = pd.merge(df2, sp500, on='Ticker', how='outer')
print(sp500merged)
print(sp500merged.columns)
#  add columns for 1YR change in price and market capitalization so we can do further analysis
sp500merged['One Year Change'] = sp500merged['Ticker'].apply(one_year_change)
sp500merged['Share Float'] = sp500merged['Ticker'].apply(share_float)
# Now let's quickly pull the same information for our baseline S&P500 & sector funds for comparison
# the 11 industries of the S&P 500 have their own sub-indices represented by their respective Exchange Traded Funds ETFs
industry_indexes = {'S&P 500': 'SPY', 'Communication Services': 'XLC', 'Consumer Discretionary': 'XLY',
                    'Consumer Staples': 'XLP', 'Energy': 'XLE', 'Financials': 'XLF', 'Health Care': 'XLV',
                    'Industrials': 'XLI', 'Materials': 'XLB', 'Real Estate': 'XLRE', 'Information Technology':
                    'XLK', 'Utilities': 'XLU'}
indices_and_data = []
for ticker in industry_indexes.values():
    print(ticker)
    index_data = get_stock_data(ticker)
    index_data.insert(0, ticker)
    indices_and_data.append(index_data)
    print(index_data)
#  this will be a separate dataframe for index data, which will be our performance baseline for analysis
df3 = pd.DataFrame(indices_and_data, columns=['Ticker', 'Current Price', 'Day Change', "Target Price",
                                              "Target Proximity", 'Avg Volume', 'Price Earnings Ratio', 'Rating',
                                              'Valuation'])
df3['One Year Change'] = df3['Ticker'].apply(one_year_change)
print(df3)
print(df3.info())
# Now let's write to a file and then begin the cleaning process!
sp500merged.to_csv('dataforcleaning.csv', index=False)
df3.to_csv('indexdata.csv', index=False)
print('!' * 50)
print('This concludes phase 1 of the project!')
print('Proceed to KWP510datacleaning.py and follow instructions!')
#  Information below is for further analysis beyond the scope of this project
#  creation_date = dt.date.today().strftime('%d%m%Y') #  for daily scraping and repository building
#  sp500merged.to_csv(f'foranalysis{creation_date}.csv', index=False)
#  sp500merged.to_csv('testanalysis.csv', index=False)  # for testing


