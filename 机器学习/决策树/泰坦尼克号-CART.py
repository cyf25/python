#导入工具包
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
#导入数据
data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\train.csv')
# print(data.head())
# data.info()
#数据预处理
#特征工程
x=data[['Pclass','Age','Sex']]
y=data['Survived']
#导入数据
data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\train.csv')
# print(data.head())
# data.info()
#数据预处理
#特征工程
x=data[['Pclass','Age','Sex']]
y=data['Survived']
x['Age'].fillna(x['Age'].mean(),inplace=True)
x=pd.get_dummies(x,dtype='int64')
print(x.head())
train_x,test_x,train_y,test_y=train_test_split(x,y,test_size=0.2)
#模型训练 CART
model=DecisionTreeClassifier()
model.fit(train_x,train_y)
#模型预测
y_predict=model.predict(test_x)
y1=model.predict_proba([[3,20,1,0]])
#模型评估
score=accuracy_score(test_y,y_predict)
print(score)
roc=roc_auc_score(test_y,y_predict)
print(roc)
report=classification_report(test_y,y_predict)
print(report)
print(y1)
print(y_predict)
