import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# read in the outputs of our analysis and quickly assess our portfolio to compare to index
df = pd.read_csv('dataforvisualization.csv')  # main data set
df2 = pd.read_csv('dataforvisualization1.csv')  # very small
my_portfolio = pd.read_csv('myportfolio.csv')  # based on your previous selections!
port_option_performance = pd.read_csv('portfolio_options_performance.csv')  # to compare relative performance of options
my_port_by_sector = my_portfolio.groupby('Sector')['Market Capitalization'].sum().reset_index()
my_port_by_sector.columns = ['Sector', 'Market Capitalization']
my_port_by_sector = my_port_by_sector.sort_values(by='Market Capitalization', ascending=False)
my_port_total_mc = my_port_by_sector['Market Capitalization'].sum()
my_port_by_sector['% of S&P 500'] = my_port_by_sector['Market Capitalization'] / my_port_total_mc
my_port_by_sector.rename(columns={'% of S&P 500': '% of Portfolio'}, inplace=True)
# we will create a combined df that will allow us to quickly identify our selections in context
df['Key'] = 'S&P 500'
my_portfolio['Key'] = 'My Portfolio'
combined_df = pd.concat([df, my_portfolio], keys=['S&P 500', 'My Portfolio'])  # diff our selection from the index
# the first chart will show a histogram of one year performance of the companies in the S&P 500, by Sector (hue)
fig1 = plt.figure(1)
plt.title('One Year Price Change of Companies in the S&P 500')
sns.histplot(data=df, x='One Year Change', hue='Sector', bins=50, alpha=.5)
#  the second figure will side by side the sector allocations, by market cap, for the SP500 and our portfolio
colors = ['red', 'chocolate', 'navajowhite', 'gold', 'lawngreen', 'olive', 'turquoise', 'teal', 'dodgerblue',
           'mediumpurple', 'fuchsia']  # NICE
fig, axes = plt.subplots(1, 2, figsize=(15, 5))  # create two subplots
# first chart
axes[0].pie(df2['Market Capitalization'], labels=df2['Sector'], autopct='%1.1f%%', labeldistance=1.1, pctdistance=.85,
        colors=colors)
axes[0].set_title('Market Cap of S&P 500, by Sector')
# second chart
axes[1].pie(my_port_by_sector['Market Capitalization'], labels=my_port_by_sector['Sector'], autopct='%1.1f%%',
        labeldistance=1.1, pctdistance=.85, colors=colors)
axes[1].set_title('Market Cap of Personalized Portfolio, by Sector')
plt.axis('equal')
plt.show()
# third figure will show rating to 1YC, with trendline
fig3 = plt.figure(3)
plt.title('One Year Change (%) by Rating with Trendline')
sns.regplot(x=df['One Year Change'], y=df['Rating'], ci=False, line_kws={'color': 'red'})
plt.show()
# fourth will show volume to PE ratio, size as market cap
fig4 = plt.figure(4)
plt.title('Volume to One Year Change- Market Cap as Size')
sns.scatterplot(data=df, x='Avg Volume', y='One Year Change', size='Market Capitalization')
plt.legend(loc='upper right')
plt.show()
# fifth will be a chart of 1YC sorted into 11 Sectors, hue set to index vs. our portfolio

fig5 = plt.figure(5, figsize=(6, 8))
plt.title('One Year Change of S&P 500 and Personalized Portfolio, by Sector')
ax = sns.stripplot(data=combined_df, x='Sector', y='One Year Change', hue='Key')
ax.axhline(y=0, color='r', linestyle='-')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(), rotation=-45)
plt.show()

# sixth is a bar chart showing the historical returns of the 10 different available strategies and the SP500 index
fig6 = plt.figure(6, figsize=(5, 7))
plt.title('One Year Change of 10 Available Strategies and S&P 500 Index')
port_option_performance = port_option_performance.sort_values('One Year Change')
ax = sns.barplot(data=port_option_performance, x='Strategy', y='One Year Change', palette='PiYG')
ax.axvline(x=6, color='r', linestyle='-')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(), rotation=-45)
plt.subplots_adjust(bottom=0.3)
plt.show()
