import pandas as pd
df = pd.read_csv('cleaned_data.csv')
a = df["ukupno_placeno"]
b = df["broj_nocenja"]
c = float(0)
for i in range(len(a)):
    c+= a[i] * b[i]
print(c) 