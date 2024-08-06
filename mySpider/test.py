
import pandas as pd

df = pd.read_csv('output.csv', encoding='utf-8')
last_time = df['notice_time'].iloc[-1]
last_time = pd.to_datetime(last_time)
print(df['notice_time'])