import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,roc_auc_score,classification_report
from sklearn.ensemble import AdaBoostClassifier
#导入数据
data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\wine0501.csv')
data.columns = ['Class label', 'Alcohol', 'Malic acid', 'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols',
'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity', 'Hue', 'OD280/OD315 of diluted wines',
'Proline']
data=data[data['Class label'] != 1]
x=data[['Alcohol', 'Hue']].values.copy()
y=data['Class label'].values.copy()
#将标签进行二值化（0,1）
labe=LabelBinarizer()
y=labe.fit_transform(y)
#将数据分割为训练集和测试集
train_x,x_test,train_y,test_y=train_test_split(x,y,test_size=0.2)
#模型训练
#决策树
model1=DecisionTreeClassifier()
model1.fit(train_x,train_y)
#AdaBoost
model2=AdaBoostClassifier()
model2.fit(train_x,train_y)
#模型预测
y_pre1=model1.predict(x_test)
y_pre2=model2.predict(x_test)
#模型评估
score1=accuracy_score(test_y,y_pre1)
score2=accuracy_score(test_y,y_pre2)
print(score1,score2)

 