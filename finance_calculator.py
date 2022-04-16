# Project monthy and annual expenses to estimate lifetime Net worth
# Desired Features
## Summary Values
### Annual Savings
## Accounts and Account Balances
## House purchase projection
## Credit card bonus savings
## Future Salary
## Stock Options Growth
## Investment Growth
## Inflation Adjustments

from pickle import TRUE
import matplotlib.pyplot as plt
from matplotlib.patches import StepPatch
plt.close("all")
import pandas as pd

filename = 'transactions_example'
transactions = pd.read_csv(f'{filename}.csv')

# Convert date strings to datetime objects
transactions['Start Date'] = pd.to_datetime(transactions['Start Date'], infer_datetime_format=True)
transactions['End Date'] = pd.to_datetime(transactions['End Date'], infer_datetime_format=True)

# convert period string to relativedelta object
periods = {
    "day": 'D',
    "week": 'W',
    "month": 'M',
    "year": 'Y',
    "once": 'D'
}
transactions['Period'] = [periods[row['Period']] for index, row in transactions.iterrows()]

# Convert values to positive or negative based on "Income" or "Expense"
transaction_category = {
    "Income": 1,
    "Expense": -1,
    "Asset": 1
} 
transactions['Value'] = [transaction_category[row['Category']]*row['Value'] for index, row in transactions.iterrows()]

# Instantiate variables for for loop
time_series = pd.date_range(start=transactions['Start Date'][0], end=transactions['End Date'][0], freq=transactions['Period'][0])
df = pd.DataFrame([0 for i in range(len(time_series))], index=time_series)
dfs = []

# Create list a of dataframes of each time series of recurring transactions
for index, row in transactions.iterrows():
    time_series = pd.date_range(start=transactions['Start Date'][index], end=transactions['End Date'][index], freq=transactions['Period'][index])
    df = pd.DataFrame([row['Value'] for i in range(len(time_series))], index=time_series)
    # Prototype interest rate calculation
    #df = pd.DataFrame([row['Value'] * (row['Interest Rate']/100+1) for i in range(len(time_series))], index=time_series)
    dfs.append(df)

# Create a dataframe of running total
df_total = pd.concat(dfs, axis=1)
df_sum = df_total.sum(axis=1)
df_cum = df_sum.cumsum()

# Plot income over time
x = df_cum.index.to_list()
y = df_cum.to_list()
plt.step(x, y, where='post')
plt.title("Net Worth")
plt.ylabel("Money ($)")
plt.xlabel("Date")
plt.grid(True, which='both', axis='both')
plt.xticks(rotation = 45)
plt.savefig(filename)
plt.show()