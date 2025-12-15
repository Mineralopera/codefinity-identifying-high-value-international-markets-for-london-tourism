import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("international-visitors-london.csv")

# 1 Identifying top 10 origin markets by total visitors (all years)

top_markets = df.groupby(['market'])['visits'].sum().sort_values(ascending=False).head(10)

print(f'These are the top 10 origin markets by total visitors across all years: {top_markets}')

# 2 Calculating yearly visitors per country each year
yearly_visitors_df = df[df['market'].isin(top_markets.index)]
yearly_visitors = yearly_visitors_df.groupby(['year','market'])['visits'].sum().reset_index()

# 2.1 Turning rows into columns
yearly_visitors_pv = yearly_visitors.pivot(index='year', columns='market', values='visits')

# 2.1.1 Calculating first and last year
yearly_visitors_max = yearly_visitors_df['year'].max()
yearly_visitors_min = yearly_visitors_df['year'].min()

# 2.2 Plotting the graph
yearly_visitors_pv.plot(figsize=(8, 5))
plt.xticks(range(yearly_visitors_min, yearly_visitors_max + 1, 2))
plt.title("Yearly visit trends over time top markets")
plt.xlabel("Years")
plt.margins(x=0)
plt.ylabel("Visits (x1000)")
plt.axhline(1000, color='black', linestyle='--', linewidth=0.5, label='1,000 (thousands)')
plt.legend(title="Market", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 2.3 Determining how many markets exceeded one million visits
excess = yearly_visitors_pv > 1000
markets_ae = excess.any()
count_emarkets = markets_ae.sum()
exceeded_markets = markets_ae[markets_ae].index.tolist()

print(f'Count of markets exceeding 1 million: {count_emarkets}')
print(f'Markets exceeding 1 million: {exceeded_markets}')

# 3 Calculate CAGR
first_value = yearly_visitors_pv.loc[yearly_visitors_min]
end_value = yearly_visitors_pv.loc[yearly_visitors_max]
number_years = yearly_visitors_max - yearly_visitors_min

CAGR = ((end_value / first_value) ** (1 / number_years) - 1) * 100

print(f'This is a list of the top 10 countries CAGR: {CAGR}')
print(f'This is the country with the highest CAGR: {CAGR.idxmax()}')

# 4 Stay duration and purposes
visit_purpope = df.groupby(['dur_stay', 'purpose'])['purpose'].count().reset_index(name='count')

visit_purpope_pv = visit_purpope.pivot(index='dur_stay', columns='purpose', values='count')

print(visit_purpope)

# 4.1 Visualising the visit / purpose data

