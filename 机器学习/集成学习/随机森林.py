import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
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
#随机森林模型
rf=RandomForestClassifier(n_estimators=70,max_depth=7)
rf.fit(x_train,y_train)
#交叉验证网络搜索
rf1=GridSearchCV(rf,{'n_estimators':[10,20,30,40,50,60,70,80,90,100],'max_depth':[3,4,5,6,7,8,9,10]},cv=5)
rf1.fit(x_train,y_train)
print(rf1.best_params_)
#决策树模型
dt=DecisionTreeClassifier()
dt.fit(x_train,y_train)
#模型评估
print('随机森林模型准确率：',accuracy_score(y_test,rf.predict(x_test)))
print('决策树模型准确率：',accuracy_score(y_test,dt.predict(x_test)))
print('随机森林网络搜索模型准确率：',accuracy_score(y_test,rf1.predict(x_test)))
