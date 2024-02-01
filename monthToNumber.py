from time import strptime

import pandas as pd

df = pd.read_csv(r'C:\Users\alial\OneDrive\Desktop\Umsatzprognose_2\Umsatzprognose\Täglicher_Umsatz_2014_2023.csv', delimiter=';')
print(df)




df['month_number'] = [strptime(str(x), '%b').tm_mon for x in df['Monat']]
df = df.drop('Monat', axis=1)
print(df)