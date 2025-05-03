import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
#d导入数据
data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\train.csv')
#查看数据
# data.info()
#数据预处理
x=data[['Pclass','Age','Sex']].copy()
y=data['Survived'].copy()
#填补缺失值
x['Age'].fillna(x['Age'].mean(),inplace=True)
#热编码
x=pd.get_dummies(x,dtype='int64')
#划分数据集
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
#模型训练
model=GradientBoostingClassifier()
model.fit(x_train,y_train)
#模型评估
y_pre=model.predict(x_test)
score=accuracy_score(y_test,y_pre)
print(score)