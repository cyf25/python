import pandas as pd
import numpy as np
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def load_data(file_path):
    """
    加载数据并处理评价列
    :param file_path: 数据文件路径
    :return: 加载并处理后的数据
    """
    data = pd.read_csv(file_path, encoding='gbk')
    data['评价'] = data['评价'].apply(lambda x: 1 if x == '好评' else 0)
    return data


def load_stopwords(stopwords_path):
    """
    加载停用词
    :param stopwords_path: 停用词文件路径
    :return: 停用词列表
    """
    stopwords = []
    with open(stopwords_path, 'r', encoding='utf_8') as f:
        lines = f.readlines()
        for line in lines:
            stopwords.append(line.strip())
    return list(set(stopwords))


def preprocess_text(data, stopwords):
    """
    对文本进行分词并去除停用词
    :param data: 包含文本的数据集
    :param stopwords: 停用词列表
    :return: 处理后的文本列表
    """
    comment_list = []
    for tmp in data['内容']:
        seg_list = jieba.cut(tmp, cut_all=False)
        seg_list = [word for word in seg_list if word not in stopwords]
        comment_list.append(' '.join(seg_list))
    return comment_list


def extract_features(text_list, stopwords):
    """
    统计词频并返回特征矩阵和特征名称
    :param text_list: 处理后的文本列表
    :param stopwords: 停用词列表
    :return: 特征矩阵和特征名称
    """
    con = CountVectorizer(stop_words=stopwords)
    X = con.fit_transform(text_list)
    name = con.get_feature_names_out()
    return X, name


def split_data(X, y, split_index):
    """
    划分训练集和测试集 
    :param X: 特征矩阵
    :param y: 标签
    :param split_index: 划分索引
    :return: 训练集和测试集的特征和标签
    """
    x_train = X[:split_index, :]
    x_test = X[split_index:, :]
    y_train = y[:split_index]
    y_test = y[split_index:]
    return x_train, x_test, y_train, y_test


def train_model(x_train, y_train):
    """
    训练朴素贝叶斯模型
    :param x_train: 训练集特征
    :param y_train: 训练集标签
    :return: 训练好的模型
    """
    model = MultinomialNB(alpha=1.0)
    model.fit(x_train, y_train)
    return model


def evaluate_model(model, x_test, y_test):
    """
    评估模型并返回预测值
    :param model: 训练好的模型
    :param x_test: 测试集特征
    :param y_test: 测试集标签
    :return: 预测值
    """
    y_predict = model.predict(x_test)
    print('预测值：', y_predict)
    print('真实值：', y_test)
    return y_predict


if __name__ == "__main__":
    file_path = r'D:\BaiduNetdiskDownload\day4\书籍评价.csv'
    stopwords_path = r'D:\BaiduNetdiskDownload\day4\stopwords.txt'
    data = load_data(file_path)
    stopwords = load_stopwords(stopwords_path)
    comment_list = preprocess_text(data, stopwords)
    X, _ = extract_features(comment_list, stopwords)
    good_or_bad = data['评价'].values
    x_train, x_test, y_train, y_test = split_data(X.toarray(), good_or_bad, 10)
    model = train_model(x_train, y_train)
    evaluate_model(model, x_test, y_test)