#导入工具包
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score

#导入数据
data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\churn.csv')
#查看数据
# data.head()
# data.info()
#数据预处理
data=pd.get_dummies(data,dtype='int64')
data=data.drop(['Churn_No','gender_Male'],axis=1)
data=data.rename(columns={'Churn_Yes':'flag'})
# print(data.head())
# print(data.info())
#特征工程
# sns.pairplot(data=data,vars=['PaymentElectronic','Contract_Month','internet_other'],hue='flag')
# plt.show()
x=data[['PaymentElectronic','Contract_Month','internet_other']]
y=data['flag']
#训练集划分
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=22,test_size=0.2)
#模型训练
model=LR()
model.fit(x_train,y_train)
#模型预测
y_predict=model.predict(x_test)
#模型评估
score=accuracy_score(y_test,y_predict)
print(score)
print(roc_auc_score(y_test,y_predict))
print(classification_report(y_test,y_predict))

