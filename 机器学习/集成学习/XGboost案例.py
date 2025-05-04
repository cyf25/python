import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.utils import class_weight
import numpy as np

# #导入数据,对数据进行预处理
# data=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\红酒品质分类.csv')
# data.info()
# x=data.iloc[:,:-1]
# y=data.iloc[:,-1]-3
# x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,stratify=y,random_state=22)
# # 3. 存储数据
# pd.concat([x_train, y_train], axis=1).to_csv(r'D:\BaiduNetdiskDownload\day4\红酒品质分类-train.csv')
# pd.concat([x_test, y_test], axis=1).to_csv(r'D:\BaiduNetdiskDownload\day4\红酒品质分类-test.csv')
data_train=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\红酒品质分类-train.csv')
data_test=pd.read_csv(r'D:\BaiduNetdiskDownload\day4\红酒品质分类-test.csv')
# #模型训练
x_train=data_train.iloc[:,:-1]
y_train=data_train.iloc[:,-1]
x_test=data_test.iloc[:,:-1]
y_test=data_test.iloc[:,-1]

# #模型训练
model=xgb.XGBClassifier(n_estim=100,
                        objective='multi:softmax',
                        eval_metric='merror',
                        random_state=22,
                        use_label_encoder=False)
model.fit(x_train,y_train)
#超参数选择
param_grid={
    'max_depth': np.arange(3, 5, 1),
    'n_estimators': np.arange(50, 150, 50),
    'eta': np.arange(0.1, 1, 0.3)
}
grid_search=GridSearchCV(model,param_grid,scoring='accuracy',cv=5)
grid_search.fit(x_train,y_train)
print(grid_search.best_params_)
#模型评估
y_pred=model.predict(x_test)
y_pred1=grid_search.predict(x_test)
print(classification_report(y_test,y_pred1))
print(classification_report(y_test,y_pred))
