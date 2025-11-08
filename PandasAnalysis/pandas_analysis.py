import pandas as pd

df = pd.read_csv('matches.csv', index_col='id')

# Question 1:

# Number of matches in csv
number_of_matches_in_csv = len(df.iloc[:, 0])

# Coulmn names
column_list = df.columns
column_names = [print(i, end=" ") for i in df.columns]    # to print the column names

# first 5 rows of the data
first_five_rows = df.iloc[:5]
print(first_five_rows)

# describe the data
print(df.describe())




# Question 2: Which player has won the most "Player of the Match" awards in 
# games decided on the final ball (i.e., matches won by just 1 run or 1 wicket).
POTM = []

a = df['win_by_wickets']==1
b = df['win_by_runs'] == 1
c = (a.__or__(b))
print(df.mask(c))



