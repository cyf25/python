#导入工具包
#分类
from  sklearn.neighbors import KNeighborsClassifier
#回归
from sklearn.neighbors import KNeighborsRegressor
#数据
x_train=[[1,2],[1.5,1.8],[5,8],[8,8],[1,0.6],[9,11]]
y_train=[0,0,1,1,0,1]
x1_trai=[[2],[6],[8]]
y1_train=[2,3,4]
#实例化
model=KNeighborsClassifier(n_neighbors=3)
model1=KNeighborsRegressor(n_neighbors=1)

#训练
model.fit(x_train,y_train)
model1.fit(x1_trai,y1_train)
#预测
y_pred=model.predict([[2,2],[6,9]])
y_pred1=model1.predict([[10],[6],[8]])
print(y_pred)
print(y_pred1)