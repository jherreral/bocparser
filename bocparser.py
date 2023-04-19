import pandas as pd

# Specify the range of cells to read
cell_range = 'B:K'
rows_to_skip=17
# Read the range of cells into a Pandas DataFrame
df = pd.read_excel('saldo.xls', skiprows=rows_to_skip,usecols=cell_range)
df.drop(axis=1, index=3,inplace=True)
# Print the DataFrame
print(df)