# 0 导入工具包
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 1.数据
x = np.array(list(range(1,11))).reshape(-1,1)
y = np.array([5.56, 5.70, 5.91, 6.40, 6.80, 7.05, 8.90, 8.70, 9.00, 9.05])


# 2.模型训练
model1 = DecisionTreeRegressor(max_depth=1)
model2 = DecisionTreeRegressor(max_depth=3)
model3 = LinearRegression()

model1.fit(x,y)
model2.fit(x,y)
model3.fit(x,y)


# 3.模型预测
x_test = np.arange(0.0, 10.0, 0.01).reshape(-1, 1)
print(x_test)
y_pre1 = model1.predict(x_test)
print(y_pre1)
y_pre2 = model2.predict(x_test)
print(y_pre2)
y_pre3 = model3.predict(x_test)
print(y_pre3)


# 4.可视化
plt.figure(figsize=(10, 6), dpi=100)
plt.scatter(x, y, label='data')
plt.plot(x_test, y_pre1,label='max_depth=1')  # 深度1层
plt.plot(x_test, y_pre2, label='max_depth=3')   # 深度3层
plt.plot(x_test, y_pre3, label='linear')
plt.xlabel('data')
plt.ylabel('target')
plt.title('DecisionTreeRegressor')
plt.legend()
plt.show()
