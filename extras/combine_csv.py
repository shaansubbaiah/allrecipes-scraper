import pandas as pd

# just included for reference
# this can be improved by using loops, reading the dir for CSV files.

# read the created CSV files 
df1 = pd.read_csv('1.csv')

print(df1.head())
print(len(df1))

df2 = pd.read_csv('2.csv')

print(df2.head())
print(len(df2))

df3 = pd.read_csv('3.csv')

print(df3.head())
print(len(df3))

print(f'total: {len(df1)+len(df2)+len(df3)}')

# generate a single combined CSV
df4 = pd.concat([df1, df2, df3])
print(df4.head())
combined_len = len(df4)
print(combined_len)

# drop duplicated entries if any
df4 = df4.drop_duplicates()
print(df4.head())
unique_len = len(df4)
print(unique_len)
print(f'unique% = {unique_len/combined_len*100}')

df4.to_csv('combined.csv', index=False)

# view the combined CSV with unique entries
df5 = pd.read_csv('combined.csv')
print(df5.head())
print(len(df5))

# # Scraped from /recipes
# name  ... omega_6_fatty_acid_g
# 0  Simple Macaroni and Cheese  ...                  NaN
# 1    Gourmet Mushroom Risotto  ...                  NaN
# 2              Dessert Crepes  ...                  NaN
# 3                 Pork Steaks  ...                  NaN
# 4  Quick and Easy Pizza Crust  ...                  NaN

# [5 rows x 47 columns]
# 8895

# # Scraped from every other main category
# name  ... omega_6_fatty_acid_g
# 0                              Dessert Crepes  ...                  NaN
# 1                      Thin-Crust Pizza Dough  ...                  NaN
# 2        Chocolate-Covered Raspberry Brownies  ...                  NaN
# 3  Käsesahnetorte(German Yogurt Mousse Cake)  ...                  NaN
# 4      Brazilian Cheese Bread(Pao de Queijo)  ...                  NaN

# [5 rows x 47 columns]
# 29188

# # Scraped from appetizers-and-snacks category
# name  ... omega_6_fatty_acid_g
# 0           Perfect Pot Stickers  ...                  NaN
# 1                 Dessert Crepes  ...                  NaN
# 2  Curried Chicken Lettuce Wraps  ...                  NaN
# 3           Best Ever Crab Cakes  ...                  NaN
# 4       Scrumptious Salmon Cakes  ...                  NaN

# [5 rows x 47 columns]
# 8062

# # Total rows, main + appetizer category + other categories
# total: 46145

# # Combined CSV
# name  ... omega_6_fatty_acid_g
# 0  Simple Macaroni and Cheese  ...                  NaN
# 1    Gourmet Mushroom Risotto  ...                  NaN
# 2              Dessert Crepes  ...                  NaN
# 3                 Pork Steaks  ...                  NaN
# 4  Quick and Easy Pizza Crust  ...                  NaN

# [5 rows x 47 columns]
# 46145

# # Combined CSV without duplicates
# name  ... omega_6_fatty_acid_g
# 0  Simple Macaroni and Cheese  ...                  NaN
# 1    Gourmet Mushroom Risotto  ...                  NaN
# 2              Dessert Crepes  ...                  NaN
# 3                 Pork Steaks  ...                  NaN
# 4  Quick and Easy Pizza Crust  ...                  NaN

# [5 rows x 47 columns]
# 35516
# unique % = 76.96608516632355
