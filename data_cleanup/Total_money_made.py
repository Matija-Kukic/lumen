import pandas as pd
df = pd.read_csv('cleaned_data.csv')
df = df[df["status_rezervacije"] == 'Check-Out']
a = list(df["ukupno_placeno"])
b = list(df["broj_nocenja"])
c = float(0)
for i in range(len(a)):
    c += a[i] * b[i]
print(c) 
