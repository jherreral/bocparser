import pandas as pd
import json


def load_categories():
    """Load categories from standard and personal files."""
    with open("categories.json", "r") as infile:
        main_categories = json.load(infile)

    with open("personal.json", "r") as infile:
        personal_categories = json.load(infile)

    categories = {}

    for key, value in main_categories.items():
        if key in personal_categories:
            categories[key] = value + personal_categories[key]
        else:
            categories[key] = value

    for key, value in personal_categories.items():
        if key not in main_categories:
            categories[key] = value

    #  Make all keywords lowercase for easier comparison
    for _, keywords in categories.items():
        for i in range(len(keywords)):
            keywords[i] = keywords[i].lower()

    return categories


def get_category(description, categories):
    """Get the category for the description."""
    lowcase_description = description.lower()
    for category, word_list in categories.items():
        for word in word_list:
            if lowcase_description.find(word) != -1:
                return category
    return None


def categorizeMovements(df: pd.DataFrame, categories: dict):
    """Add the 'Rubro' field to each entry of the df ."""
    mask = df.apply(lambda row: get_category(row["Descripción"], categories), axis=1)
    df["Rubro"] = mask

    # Report results
    classified_values = df['Rubro'].notna().sum()
    unclassified_values = df['Rubro'].isna().sum()
    print(f"Classified values: {classified_values}")
    print(f"Unclassified values: {unclassified_values}")


# Main
all_categories = load_categories()

# Read the bank movements from an Excel file
cell_range = "B:K"
rows_to_skip = 17
df = pd.read_excel("saldo.xls", skiprows=rows_to_skip, usecols=cell_range)

# Clean up table
df.rename(columns={"Unnamed: 10": "Monto"}, inplace=True)
df.drop(columns=["Unnamed: 3", "Unnamed: 5", "Unnamed: 9", "Monto ($)"], inplace=True)

# Categorize movements according to type
categorizeMovements(df, all_categories)

# Print the DataFrame
print("All rows:")
print(df)

print("Unclassified rows:")
print(df[df['Rubro'].isna()])
