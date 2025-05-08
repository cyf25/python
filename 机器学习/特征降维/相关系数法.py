import pandas as pd
from sklearn.datasets import load_iris
from scipy.stats import pearsonr
from scipy.stats import spearmanr

def calculate_pearson_correlation(data, feature1, feature2):
    """
    计算两个特征之间的皮尔逊相关系数。
    
    参数:
    data : pandas DataFrame
        包含特征的数据集。
    feature1 : str
        第一个特征的名称。
    feature2 : str
        第二个特征的名称。
    
    返回:
    corr : tuple
        包含相关系数和双尾p值的元组。
    """
    corr = pearsonr(data[feature1], data[feature2])
    return corr

def calculate_spearman_correlation(data, feature1, feature2):
    """
    计算两个特征之间的斯皮尔曼相关系数。
    
    参数:
    data : pandas DataFrame
        包含特征的数据集。
    feature1 : str
        第一个特征的名称。
    feature2 : str
        第二个特征的名称。
    
    返回:
    corr : tuple
        包含相关系数和双尾p值的元组。
    """
    corr = spearmanr(data[feature1], data[feature2])
    return corr

# 加载数据
data = load_iris()
data = pd.DataFrame(data.data, columns=data.feature_names)

# 使用函数计算相关系数
corr_pearson = calculate_pearson_correlation(data, 'sepal length (cm)', 'sepal width (cm)')
corr_spearman = calculate_spearman_correlation(data, 'sepal length (cm)', 'sepal width (cm)')

print("皮尔逊相关系数:", corr_pearson, "斯皮尔曼相关系数:", corr_spearman)
