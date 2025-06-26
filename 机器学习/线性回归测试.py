import 线性回归 as lr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import 数据预处理 as yc

if __name__ == '__main__':
    # 读取数据
    data = pd.read_excel(r'D:\BaiduNetdiskDownload\day4\会员消费报表.xlsx')
    
    # 数据预处理
    preprocessor = yc.dataed()
    processed_data = preprocessor.dataed(data)
    print(processed_data.head())
    
    # 确定特征X和目标y - 使用实际列名替换'特征列'和'目标列'
    X = processed_data[['当前积分']].values  # 替换为实际特征列名，确保是二维数组
    y = processed_data['消费金额'].values    # 替换为实际目标列名
    
    # 拟合模型
    model = lr.LinearRegression(learning_rate=0.1, n_iterations=50)
    model.fit(X, y)
    
    # 预测（使用与训练数据相同特征的示例）

    X_new = np.array([[2531], [800]]).reshape(-1, 1)  # 保持二维结构
    y_pred = model.predict(X_new)
    print(f"预测结果: {y_pred[0]:.4f}")
    print(f"权重: {model.weights[0]:.4f}")
    print(f"偏置: {model.bias:.4f}")
    
    # 绘制结果
    plt.scatter(X, y, alpha=0.5)
    plt.plot(X_new, y_pred, 'r-', linewidth=2, label='预测线')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend()
    plt.show()
    
    # 绘制损失曲线
    model.plot_loss()