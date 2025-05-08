import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold

data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\垃圾邮件分类数据.csv')

transformer=VarianceThreshold(threshold=0.2)

data=transformer.fit_transform(data)
print(data.shape)
