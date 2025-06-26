#导入工具包
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
#加载数据
iris_data=load_iris()
data=pd.DataFrame(iris_data.data,columns=iris_data.feature_names)
#数据展示
data['target']=iris_data.target
print(data.head())
#数据预处理
x_train,x_test,y_train,y_test=train_test_split(iris_data.data,data.target,test_size=0.3,random_state=22)
#特征工程
ss=StandardScaler()
x_train=ss.fit_transform(x_train)
x_test=ss.transform(x_test)
#模型训练
model=KNeighborsClassifier(n_neighbors=2)
#交叉验证网络搜索,找出最合适的超参数
paras_grid={'n_neighbors':[1,3,5,7,9]}
estimator=GridSearchCV(model,paras_grid,cv=4)
estimator.fit(x_train,y_train)
#模型评估
y_pred=estimator.predict(x_test)
print(accuracy_score(y_test,y_pred))
print(estimator.best_score_)
print(estimator.best_params_)
print(estimator.best_estimator_)
print(estimator.cv_results_)
#模型测试