import pandas as pd

s = pd.read_csv('../final_data/final_result.csv')
s.drop('所属行业', axis=1, inplace=True)  # 暂时先不处理所属行业
s.dropna(axis=0, inplace=True)
cnt = 1
for index in s.index:
    s.loc[index, 'id'] = cnt
    cnt += 1
s.to_csv('../final_data/result.csv', index=False)
