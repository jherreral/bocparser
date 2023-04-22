import pandas as pd

categories = {"Delivery":["RAPPI","KUSHKI *JUSTO","MARKET CONDELL"],"Supermercado":["JUMBO"]}

def get_category(description):
    for category,word_list in categories.items():
        for word in word_list:
            if description.find(word) != -1:
                return category
    return None


def categorizeMovements(df:pd.DataFrame):
    mask = df.apply(lambda row: get_category(row['Descripción']),axis=1)
    df['Rubro'] = mask

# Read the bank movements from an Excel file
cell_range = 'B:K'
rows_to_skip=17
df = pd.read_excel('saldo.xls', skiprows=rows_to_skip,usecols=cell_range)

# Clean up table
df.rename(columns={"Unnamed: 10":"Monto"},inplace=True)
df.drop(columns=['Unnamed: 3','Unnamed: 5','Unnamed: 9','Monto ($)'],inplace=True)

# Categorize movements according to type
categorizeMovements(df)

# Print the DataFrame
print(df)