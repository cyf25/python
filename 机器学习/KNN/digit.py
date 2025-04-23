#工具包
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
# from sklearn.externals import joblib
#加载数据
data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\手写数字识别.csv')
x=data.iloc[:,1:]
y=data.iloc[:,0]
#数据预处理
#1归一化
x=x/255
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,stratify=y,random_state=22)
#模型训练
mmodel=KNeighborsClassifier(n_neighbors=1)
#1参数调优
paras_grid={'n_neighbors':[1,3,5,7,9,11,13,15,17,19]}#参数网格
estimator=GridSearchCV(mmodel,paras_grid,cv=4)
estimator.fit(x_train,y_train)
print(estimator.best_params_)
#模型评估
print(estimator.score(x_test,y_test))
#模型预测
img=plt.imread(r'D:\BaiduNetdiskDownload\day4\demo.png',0)
img=img.reshape(1,-1)/255
y_pred=estimator.predict(img)
print(y_pred)
#模型保存
# joblib.dump(estimator,'knn_digit.pkl')
