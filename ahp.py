import pandas as pd

data = {'col1': [1, 2, 3, 4], 'col2': [5, 6, 7, 8]}
df = pd.DataFrame(data)

# ganti nilai kolom 'col1' dengan nilai baru
df['col1'].replace(1, 10, inplace=False)

print(df)
