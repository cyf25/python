import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import calinski_harabasz_score

def generate_data(n_samples=1000, n_features=2, centers=[[-1,-1],[0,0],[1,1],[2,2]], cluster_std=[0.4, 0.2, 0.2, 0.2], random_state=0):
    """
    生成随机数据
    """
    X, y = make_blobs(n_samples=n_samples, n_features=n_features, centers=centers, cluster_std=cluster_std, random_state=random_state)
    return X, y

def perform_kmeans(X, n_clusters=4, random_state=9):
    """
    执行KMeans聚类
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    kmeans.fit(X)
    y_pred = kmeans.predict(X)
    return kmeans, y_pred

def plot_clusters(X, y_pred, centers):
    """
    绘制聚类结果和聚类中心
    """
    plt.scatter(X[:, 0], X[:, 1], c=y_pred, marker='o')
    plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x')
    plt.show()

def calculate_score(X, y_pred):
    """
    计算轮廓系数
    """
    score = calinski_harabasz_score(X, y_pred)
    return score

# 主程序
if __name__ == "__main__":
    # 生成随机数据
    X, y = generate_data()

    # 执行KMeans聚类
    kmeans, y_pred = perform_kmeans(X)

    # 绘制聚类结果和聚类中心
    centers = kmeans.cluster_centers_
    plot_clusters(X, y_pred, centers)

    # 计算并打印轮廓系数
    score = calculate_score(X, y_pred)
    print("Calinski-Harabasz Score:", score)
