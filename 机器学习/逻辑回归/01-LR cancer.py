#导入工具包
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.metrics import recall_score,precision_score
#导入数据
data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\breast-cancer-wisconsin.csv')
#数据预处理
data=data.replace(to_replace='?',value=np.nan)
data=data.dropna()
#1.拆分数据
x=data.iloc[:,1:-1]
y=data['Class']
#2.测试训练数据划分
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=22,test_size=0.2)
#特征工程
#1标准化
sc=StandardScaler()
x_train=sc.fit_transform(x_train)
x_test=sc.transform(x_test)
#模型训练
#1.实例化模型
model=LR()
#2.模型训练
model.fit(x_train,y_train)
#模型评估
y_predict=model.predict(x_test)
score=accuracy_score(y_test,y_predict)
print(y_predict)
print(score)

#模型精确率
print(precision_score(y_test,y_predict,pos_label=4))
#模型召回率（查全率）
print(recall_score(y_test,y_predict,pos_label=4))

#模型F1值
print(2*precision_score(y_test,y_predict,pos_label=4)*recall_score(y_test,y_predict,pos_label=4)/(precision_score(y_test,y_predict,pos_label=4)+recall_score(y_test,y_predict,pos_label=4)))
