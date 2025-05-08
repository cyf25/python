from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

def reduce_features_by_number(X, n_components):
    """
    通过保留指定数量的特征来降维。
    
    参数:
    X : array-like, shape (n_samples, n_features)
        输入数据。
    n_components : int
        要保留的特征数量。
    
    返回:
    X_reduced : array-like, shape (n_samples, n_components)
        降维后的数据。
    """
    transformer = PCA(n_components=n_components)
    X_reduced = transformer.fit_transform(X)
    return X_reduced

def reduce_features_by_ratio(X, ratio):
    """
    通过保留指定比例的信息来降维。
    
    参数:
    X : array-like, shape (n_samples, n_features)
        输入数据。
    ratio : float
        要保留的信息比例。
    
    返回:
    X_reduced : array-like, shape (n_samples, n_components)
        降维后的数据。
    """
    transformer = PCA(n_components=ratio)
    X_reduced = transformer.fit_transform(X)
    return X_reduced

# 加载数据
x, y = load_iris(return_X_y=True)

# 使用函数降维
x_reduced_by_number = reduce_features_by_number(x, 2)
x_reduced_by_ratio = reduce_features_by_ratio(x, 0.95)

print("通过保留2个特征降维后的数据形状：", x_reduced_by_number.shape)
print("通过保留95%信息降维后的数据形状：", x_reduced_by_ratio.shape)
