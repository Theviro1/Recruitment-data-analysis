import pandas as pd
import chardet
import os

# 获取全部csv文件的路径名称
folder_path = '../data/'
csv_files_path = []
for f in os.listdir(folder_path):
    if f.endswith('.csv'):
        csv_files_path.append(folder_path + f)

# 建立全新的csv文件作为结果
result = pd.DataFrame()

# 顺序读取每一个文件并处理
for csv_path in csv_files_path:
    # 确定编码格式，这一步需要单独查看csv文件完成
    if csv_path.endswith('result1.csv') or csv_path.endswith('result2.csv'):
        encode = 'GB2312'
    else:
        encode = 'utf-8'
    s = pd.read_csv(csv_path, encoding=encode, encoding_errors='replace')  # 读取csv文件并获取到对应的dataFrame
    # 删除jobId
    if 'jobId' in s.columns:
        s.drop('jobId', axis=1, inplace=True)
    # 合成一个csv文件
    result = pd.concat([result, s], ignore_index=True)
    
result.to_csv('../final_data/final.csv', index=False)
print(result)
