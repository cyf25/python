#归一化处理
#导入工具包
from sklearn.preprocessing import MinMaxScaler
#标准化处理
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
#数据
data=[[180, 80, 1], [150, 70, 0], [170, 70, 1]]

#实例化
tranformer=MinMaxScaler(feature_range=(0,1))
tranformer1=StandardScaler()
#fit_transform处理
data_new1=tranformer1.fit_transform(data)
data_new=tranformer.fit_transform(data)
print(data_new)
print(data_new1)