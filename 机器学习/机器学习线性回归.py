import numpy as np
import matplotlib as plt
import pandas as pd


class LinearRegression:
    #初始化
    def __init__(self,learn_rate=0.01, n_iters=1000):
        self.learn_rate=learn_rate
        self.n_iters=n_iters
        self.weights=None
        self.basis=None
        self.loss_history=[]
    
    def fit(self,X,Y):
        n_samples,n_features=X.shape
        #初始化参数
        self.weights=np.zeros(n_features)
        self.basis=0
        #梯度下降
        for _ in range(self.n_iters):
            Y_pred=np.dot(X,self.weights)+self.basis
            #计算损失
            loss=np.mean((Y_pred-Y)**2)
            self.loss_history.append(loss)
            #计算梯度
            dw=(1/n_samples)*np.dot(X.T,(Y_pred-Y))
            db=(1/n_samples)*np.sum(Y_pred-Y)
            #更新参数
            self.weights-=self.learn_rate*dw
            self.basis-=self.learn_rate*db
    #预测值
    def predict(self,X):
        return np.dot(X,self.weights)+self.basis
    #绘制损失函数
    def plot_loss(self): 
        plt.plot(self.loss_history)
        plt.xlable('Iterations')
        plt.ylable('Loss')
        plt.title('Loss Function')
        plt.show()
#测试
