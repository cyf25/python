from sklearn.datasets import make_blobs
from matplotlib import pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score

## 生成数据
def generate_data(n_samples=1000, n_features=2, centers=[[-1,-1],[0,0],[1,1],[2,2]], cluster_std=[0.4, 0.2, 0.2, 0.2], random_state=0):
    x, y = make_blobs(n_samples=n_samples, n_features=n_features, centers=centers, cluster_std=cluster_std, random_state=random_state)
    return x, y

# 展示数据
def show_data(x, y):
    plt.scatter(x[:, 0], x[:, 1], c=y, cmap='viridis')
    plt.show()

# 模型训练
def perform_kmeans(X, n_clusters=4, random_state=9):
    model = KMeans(n_clusters=n_clusters, random_state=random_state)
    model.fit(X)
    return model

# 计算SSE
def calculate_sse(model):
    return 'SSE: %.3f' % model.inertia_

# 计算轮廓系数
def calculate_silhouette_score(X, y_pred):
    return 'SC: %.3f' % silhouette_score(X, y_pred)

# 计算CH指标
def calculate_calinski_harabasz_score(X, y_pred):
    return 'CH: %.3f' % calinski_harabasz_score(X, y_pred)

# 展示结果
if __name__ == '__main__':
    x, y = generate_data()
    show_data(x, y)
    model = perform_kmeans(x)
    y_pred = model.predict(x)
    print(calculate_sse(model))
    print(calculate_silhouette_score(x, y_pred))
    print(calculate_calinski_harabasz_score(x, y_pred))
