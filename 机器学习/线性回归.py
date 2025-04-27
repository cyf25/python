import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置默认字体为黑体
plt.rcParams["axes.unicode_minus"] = False    # 解决负号显示问题
class LinearRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate #学习率
        self.n_iterations = n_iterations#迭代次数
        self.weights = None #权重
        self.bias = None  #偏置
        self.loss_history = [] #损失历史记录
    
    def fit(self, X, y):
        n_samples, n_features = X.shape #样本数量和特征数量
        
        # 初始化参数
        self.weights = np.zeros(n_features) 
        self.bias = 0
        
        # 梯度下降
        for _ in range(self.n_iterations):
            # 预测值
            y_predicted = np.dot(X, self.weights) + self.bias
            
            # 计算损失 (MSE)
            loss = np.mean((y_predicted - y)**2)
            self.loss_history.append(loss)
            
            # 计算梯度
            dw = (1/n_samples) * np.dot(X.T, (y_predicted - y)).flatten()  # 添加flatten() 以使dw为一维数组 
            db = (1/n_samples) * np.sum(y_predicted - y)
            #dw是权重梯度，db是偏置梯度
            # 更新参数
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
    
    def predict(self, X):
        # 预测
        return np.dot(X, self.weights) + self.bias
    
    def plot_loss(self):
        plt.plot(range(self.n_iterations), self.loss_history)
        plt.xlabel('迭代次数')
        plt.ylabel('均方误差')
        plt.title('损失函数收敛')
        plt.show()

# if __name__ == "__main__":
#     # 生成数据并确保y是一维数组 
#     np.random.seed(42) # 设置随机种子以保证结果可复现
#     X = 2 * np.random.rand(100, 1) #
#     y = 4 + 3 * X + np.random.randn(100, 1)
#     y = y.flatten()  # 关键修改：将y从(100,1)变为(100,)
    
#     # 创建并训练模型
#     model = LinearRegression(learning_rate=0.1, n_iterations=100)
#     model.fit(X, y)
    
#     # 预测
#     X_new = np.array([[0], [2]])
#     y_pred = model.predict(X_new)
    
#     print(f"Weights: {model.weights[0]:.4f}")
#     print(f"Bias: {model.bias:.4f}")
    
#     # 绘制结果
#     plt.scatter(X, y, alpha=0.5)
#     plt.plot(X_new, y_pred, 'r-', linewidth=2, label='Predictions')
#     plt.xlabel('X')
#     plt.ylabel('y')
#     plt.legend()
#     plt.show()
    
#     # 绘制损失曲线
#     model.plot_loss()