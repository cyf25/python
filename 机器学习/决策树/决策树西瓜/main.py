import numpy as np
import pandas as pd
import math
import collections
import matplotlib.pylab as plt
import matplotlib
import copy
import os
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# 分类函数：使用决策树对新样本进行分类
def classify(input_tree, feat_labels, test_vec):
    first_str = list(input_tree.keys())[0]
    feat_index = feat_labels.index(first_str.split('=')[0])
    second_dict = input_tree[first_str]
    
    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if isinstance(second_dict[key], dict):
                class_label = classify(second_dict[key], feat_labels, test_vec)
            else:
                class_label = second_dict[key]
            return class_label
    return "未知"  # 如果没有匹配的分支

# 创建输出目录
output_dir = "决策树计算过程"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 全局变量，记录当前递归深度和节点路径
current_depth = 0
current_path = []

# 导入数据并分割训练集和测试集
def import_data(test_size=0.3, random_state=42):
    data = pd.read_csv('watermalon.txt')
    data = np.array(data).tolist()
    labels = ['色泽', '根蒂', '敲击', '纹理', '脐部', '触感']  # 特征名
    labels_full = {}  # 存储每个特征的所有可能取值
    for i in range(len(labels)):
        labelList = [example[i] for example in data]
        uniqueLabel = set(labelList)
        labels_full[labels[i]] = uniqueLabel
    
    # 分割训练集和测试集
    np.random.seed(random_state)
    np.random.shuffle(data)
    split_idx = int(len(data) * (1 - test_size))
    train_data = data[:split_idx]
    test_data = data[split_idx:]
    
    return train_data, test_data, labels, labels_full

# 计算数据集的信息熵（好瓜/坏瓜的分布熵）
def calcShannonEnt(dataSet, desc="数据集", file=None):
    numEntries = len(dataSet)
    labelCounts = collections.defaultdict(int)
    for featVec in dataSet:
        currentLabel = featVec[-1]  # 最后一列是好瓜/坏瓜标签
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key, count in labelCounts.items():
        prob = float(count) / numEntries
        shannonEnt -= prob * math.log2(prob)
    
    # 打印计算过程到控制台和文件
    log_text = f"==== {desc} 信息熵计算 ====\n"
    log_text += f"样本总数: {numEntries}\n"
    log_text += f"标签分布: {dict(labelCounts)}\n"
    log_text += f"信息熵结果: {shannonEnt:.4f}\n\n"
    
    print(log_text, end="")
    if file:
        file.write(log_text)
    
    return shannonEnt

# 按特征划分数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# 计算特征的条件熵（详细打印过程到文件）
def calcFeatureCondEntropy(dataSet, axis, featureName, labels, file=None):
    global current_depth, current_path
    numEntries = len(dataSet)
    featureValues = [example[axis] for example in dataSet]
    uniqueValues = set(featureValues)
    condEntropy = 0.0
    
    # 打印计算过程标题
    log_text = f"==== {featureName} 特征条件熵计算 ====\n"
    log_text += f"特征索引: {axis}，特征名称: {featureName}\n"
    log_text += f"特征所有可能取值: {uniqueValues}\n"
    log_text += f"总样本数: {numEntries}\n\n"
    
    print(log_text, end="")
    if file:
        file.write(log_text)
    
    for idx, value in enumerate(uniqueValues, start=1):
        subDataSet = splitDataSet(dataSet, axis, value)  # 按特征取值划分
        subSetSize = len(subDataSet)
        prob = subSetSize / float(numEntries)       # 子数据集占比
        
        # 计算子数据集的信息熵
        sub_desc = f"子数据集（{featureName}={value}）"
        subEntropy = calcShannonEnt(subDataSet, desc=sub_desc, file=file)
        
        # 累加条件熵
        condEntropy += prob * subEntropy
        log_text = f"子数据集 {idx} 贡献: {prob:.4f} * {subEntropy:.4f} = {prob * subEntropy:.4f}\n"
        log_text += f"当前累计条件熵: {condEntropy:.4f}\n\n"
        
        print(log_text, end="")
        if file:
            file.write(log_text)
    
    log_text = f"==== {featureName} 特征条件熵最终结果 ====\n"
    log_text += f"{featureName} 条件熵: {condEntropy:.4f}\n\n"
    
    print(log_text, end="")
    if file:
        file.write(log_text)
    
    return condEntropy

# 计算特征的分裂信息熵（C4.5算法需要）
def calcSplitInfo(dataSet, axis, featureName, file=None):
    """
    计算特征的分裂信息熵，用于C4.5算法的信息增益率计算
    分裂信息熵 = -sum(|Dv|/|D| * log2(|Dv|/|D|))
    """
    numEntries = len(dataSet)
    featureValues = [example[axis] for example in dataSet]
    uniqueValues = set(featureValues)
    splitInfo = 0.0
    
    log_text = f"==== {featureName} 特征分裂信息熵计算 ====\n"
    log_text += f"特征索引: {axis}，特征名称: {featureName}\n"
    log_text += f"特征所有可能取值: {uniqueValues}\n"
    log_text += f"总样本数: {numEntries}\n\n"
    
    print(log_text, end="")
    if file:
        file.write(log_text)
    
    for idx, value in enumerate(uniqueValues, start=1):
        subDataSet = splitDataSet(dataSet, axis, value)
        subSetSize = len(subDataSet)
        prob = subSetSize / float(numEntries)
        
        if prob > 0:  # 避免log2(0)
            splitInfo -= prob * math.log2(prob)
            log_text = f"子数据集 {idx}（{featureName}={value}）贡献: -{prob:.4f} * log2({prob:.4f}) = -{prob:.4f} * {math.log2(prob):.4f} = {prob * math.log2(prob):.4f}\n"
        else:
            log_text = f"子数据集 {idx}（{featureName}={value}）贡献: 0（概率为0）\n"
        
        print(log_text, end="")
        if file:
            file.write(log_text)
    
    log_text = f"==== {featureName} 特征分裂信息熵最终结果 ====\n"
    log_text += f"{featureName} 分裂信息熵: {splitInfo:.4f}\n\n"
    
    print(log_text, end="")
    if file:
        file.write(log_text)
    
    return splitInfo

# 选择最优划分特征（信息增益率 - C4.5算法）
def chooseBestFeatureToSplit(dataSet, labels, file=None):
    global current_depth, current_path
    numFeatures = len(dataSet[0]) - 1  # 最后一列是标签，不算特征
    baseEntropy = calcShannonEnt(dataSet, desc="原始数据集", file=file)  # 数据集原始熵
    bestInfoGainRatio = 0.0
    bestFeature = -1
    bestFeatureCondEntropy = {}  # 存储每个特征的条件熵
    bestFeatureSplitInfo = {}    # 存储每个特征的分裂信息熵
    
    log_text = f"\n==== 开始计算各特征信息增益率（C4.5算法） ====\n\n"
    print(log_text, end="")
    if file:
        file.write(log_text)
    
    for i in range(numFeatures):
        featureName = labels[i]
        log_text = f"\n---- 处理特征: {featureName}（索引 {i}） ----\n"
        print(log_text, end="")
        if file:
            file.write(log_text)
        
        # 计算条件熵
        condEntropy = calcFeatureCondEntropy(dataSet, i, featureName, labels, file)
        bestFeatureCondEntropy[featureName] = condEntropy
        
        # 计算分裂信息熵
        splitInfo = calcSplitInfo(dataSet, i, featureName, file)
        bestFeatureSplitInfo[featureName] = splitInfo
        
        # 计算信息增益
        infoGain = baseEntropy - condEntropy
        
        # 计算信息增益率（C4.5算法的核心）
        if splitInfo > 0:  # 避免除零
            infoGainRatio = infoGain / splitInfo
        else:
            infoGainRatio = 0.0  # 如果分裂信息熵为0，则信息增益率为0
        
        log_text = f"信息增益计算: 原始熵({baseEntropy:.4f}) - 条件熵({condEntropy:.4f}) = {infoGain:.4f}\n"
        log_text += f"信息增益率计算: 信息增益({infoGain:.4f}) / 分裂信息熵({splitInfo:.4f}) = {infoGainRatio:.4f}\n"
        print(log_text, end="")
        if file:
            file.write(log_text)
        
        if infoGainRatio > bestInfoGainRatio:
            bestInfoGainRatio = infoGainRatio
            bestFeature = i
        print("\n")
    
    # 单独打印各特征条件熵和分裂信息熵结果
    log_text = "==== 各特征条件熵和分裂信息熵汇总 ====\n"
    for feat in bestFeatureCondEntropy.keys():
        cond_entropy = bestFeatureCondEntropy[feat]
        split_info = bestFeatureSplitInfo[feat]
        info_gain = baseEntropy - cond_entropy
        info_gain_ratio = info_gain / split_info if split_info > 0 else 0.0
        log_text += f"{feat}: 条件熵={cond_entropy:.4f}, 分裂信息熵={split_info:.4f}, 信息增益={info_gain:.4f}, 信息增益率={info_gain_ratio:.4f}\n"
    log_text += f"最优特征为: {labels[bestFeature]}（信息增益率 {bestInfoGainRatio:.4f}）\n\n"
    
    print(log_text, end="")
    if file:
        file.write(log_text)
    
    return bestFeature

# 判断数据集特征是否一致（用于终止递归）
def judgeEqualLabels(dataSet):
    feature_leng = len(dataSet[0]) - 1
    data_leng = len(dataSet)
    first_feature = ''
    for i in range(feature_leng):
        first_feature = dataSet[0][i]
        for _ in range(1, data_leng):
            if first_feature != dataSet[_][i]:
                return False
    return True

# 多数表决（特征用完时，选出现最多的标签）
def majorityCnt(classList):
    classCount = collections.Counter(classList)
    return classCount.most_common(1)[0][0]

# 创建决策树（节点文本：特征=条件熵值）
def createTree(dataSet, labels):
    global current_depth, current_path
    classList = [example[-1] for example in dataSet]
    
    # 终止条件1：所有样本标签相同
    if classList.count(classList[0]) == len(classList):
        # 获取当前文件路径
        node_path = "_".join(current_path)
        file_name = f"{output_dir}/深度{current_depth}_{node_path}_计算过程.txt"
        
        # 写入终止原因到文件
        with open(file_name, "a", encoding="utf-8") as file:
            # 将标签转换为中文
            chinese_label = "好瓜" if classList[0] == "是" else "坏瓜" if classList[0] == "否" else classList[0]
            file.write(f"\n==== 终止原因：所有样本标签相同 ({chinese_label}) ====\n")
            file.write(f"样本数量: {len(dataSet)}\n")
            file.write(f"标签分布: {dict(collections.Counter(classList))}\n")
        
        # 减少递归深度
        current_depth -= 1
        
        # 返回中文标签
        return "好瓜" if classList[0] == "是" else "坏瓜" if classList[0] == "否" else classList[0]
    
    # 终止条件2：特征用完或所有特征取值一致
    if len(dataSet[0]) == 1 or judgeEqualLabels(dataSet):
        # 获取当前文件路径
        node_path = "_".join(current_path)
        file_name = f"{output_dir}/深度{current_depth}_{node_path}_计算过程.txt"
        
        # 写入终止原因到文件
        with open(file_name, "a", encoding="utf-8") as file:
            reason = "特征用完" if len(dataSet[0]) == 1 else "所有特征取值一致"
            # 获取多数标签并转换为中文
            majority_label = majorityCnt(classList)
            chinese_label = "好瓜" if majority_label == "是" else "坏瓜" if majority_label == "否" else majority_label
            file.write(f"\n==== 终止原因：{reason} ====\n")
            file.write(f"剩余特征数: {len(labels)}\n")
            file.write(f"标签分布: {dict(collections.Counter(classList))}\n")
            file.write(f"多数标签: {chinese_label}\n")
        
        # 减少递归深度
        current_depth -= 1
        
        # 返回中文标签
        return "好瓜" if majority_label == "是" else "坏瓜" if majority_label == "否" else majority_label
    
    # 增加递归深度
    current_depth += 1
    
    # 打开文件，记录当前节点的计算过程
    node_path = "_".join(current_path)
    file_name = f"{output_dir}/深度{current_depth}_{node_path}_计算过程.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        # 写入当前节点路径信息
        file.write(f"==== 当前节点路径: {' -> '.join(current_path) if current_path else '根节点'} ====\n\n")
        
        # 选最优特征
        bestFeat = chooseBestFeatureToSplit(dataSet, labels, file)
        bestFeatLabel = labels[bestFeat]
        
        # 重新计算该特征的条件熵（用于节点显示）
        condEntropy = calcFeatureCondEntropy(dataSet, bestFeat, bestFeatLabel, labels, file)
        entropyStr = f"{condEntropy:.2f}"  # 保留两位小数
        
        # 构建树结构：特征=条件熵值
        myTree = {f"{bestFeatLabel}={entropyStr}": {}}
        
        # 递归构建子树
        subLabels = labels[:]
        del (subLabels[bestFeat])  # 删除已用特征
        featValues = [example[bestFeat] for example in dataSet]
        uniqueVals = set(featValues)
        
        for value in uniqueVals:
            # 记录当前分支路径
            current_path.append(f"{bestFeatLabel}={value}")
            
            # 写入分支信息
            file.write(f"\n==== 开始处理分支: {bestFeatLabel}={value} ====\n\n")
            
            subDataSet = splitDataSet(dataSet, bestFeat, value)
            myTree[f"{bestFeatLabel}={entropyStr}"][value] = createTree(subDataSet, subLabels)
            
            # 回溯路径
            current_path.pop()
    
    # 减少递归深度
    current_depth -= 1
    return myTree

# 绘制决策树节点
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=dict(arrowstyle="<-"))

# 获取叶节点数量
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if isinstance(secondDict[key], dict):
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

# 获取树的深度
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDic = myTree[firstStr]
    for key in secondDic.keys():
        if isinstance(secondDic[key], dict):
            thisDepth = 1 + getTreeDepth(secondDic[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

# 在父子节点间添加文本信息
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

# 绘制决策树
def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, dict(boxstyle="sawtooth", fc="0.8"))
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if isinstance(secondDict[key], dict):
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, dict(boxstyle="round4", fc="0.8"))
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

# 保存决策树图片（增加中文标签支持）
def saveTreeImage(myTree, filename=f"{output_dir}/决策树可视化图.png", figsize=(12, 8), dpi=300, use_chinese=True):
    """
    将决策树保存为图片文件
    
    参数:
    myTree: 决策树字典
    filename: 保存的图片路径
    figsize: 图片大小 (宽, 高)
    dpi: 图片分辨率
    use_chinese: 是否使用中文标签
    """
    # 设置matplotlib支持中文显示
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    matplotlib.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    fig = plt.figure(1, facecolor='white', figsize=figsize)
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    
    # 计算树的宽度和高度
    plotTree.totalW = float(getNumLeafs(myTree))
    plotTree.totalD = float(getTreeDepth(myTree))
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    
    # 绘制树
    plotTree(myTree, (0.5, 1.0), '')
    
    # 保存图片
    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    print(f"决策树已保存为图片: {os.path.abspath(filename)}")
    
    # 关闭图片避免阻塞
    plt.close()
    
    return filename

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()

# 主流程
if __name__ == "__main__":
    print(f"计算过程将保存到目录: {os.path.abspath(output_dir)}")
    print("使用C4.5算法构建决策树（基于信息增益率）")
    train_data, test_data, labels, labels_full = import_data()
    labels_copy = copy.deepcopy(labels)  # 深拷贝避免原列表被修改
    
    # 训练决策树
    mytree = createTree(train_data, labels_copy)
    
    print("\n==== 最终决策树结构（C4.5算法） ====")
    print(mytree)
    
    # 保存决策树图片
    # saveTreeImage(mytree)
    
    # 测试模型
    print("\n==== 测试集评估 ====")
    true_labels = []
    pred_labels = []
    for sample in test_data:
        true_label = sample[-1]
        predicted_label = classify(mytree, labels, sample[:-1])
        true_labels.append(true_label)
        pred_labels.append(predicted_label)
    
    # 计算评估指标
    from sklearn.metrics import classification_report, confusion_matrix
    
    # 转换为中文标签
    label_map = {'是': '好瓜', '否': '坏瓜'}
    true_labels = [label_map.get(l, l) for l in true_labels]
    pred_labels = [label_map.get(l, l) for l in pred_labels]
    
    # 打印分类报告
    print("\n==== 分类报告 ====")
    print(classification_report(true_labels, pred_labels, target_names=['好瓜', '坏瓜']))
    
    # 打印混淆矩阵
    print("\n==== 混淆矩阵 ====")
    print(confusion_matrix(true_labels, pred_labels, labels=['好瓜', '坏瓜']))
    
    # 测试结果总结
    print("\n==== 详细测试结果 ====")
    print(f"数据集分割比例: 训练集70% / 测试集30%")
    total = len(train_data) + len(test_data)
    print(f"训练集样本数: {len(train_data)} ({(len(train_data)/total*100):.1f}%)")
    print(f"测试集样本数: {len(test_data)} ({(len(test_data)/total*100):.1f}%)")
    print(f"总样本数: {total}")
    print("\n测试集样本详情:")
    for i, sample in enumerate(test_data, 1):
        print(f"样本{i}: 特征={sample[:-1]}, 真实标签={sample[-1]}, 预测标签={pred_labels[i-1]}")
    
    print("\n==== 模型性能总结 ====")
    print(f"准确率: {accuracy_score(true_labels, pred_labels):.2f}")
    print(f"精确率: {precision_score(true_labels, pred_labels, pos_label='好瓜'):.2f}")
    print(f"召回率: {recall_score(true_labels, pred_labels, pos_label='好瓜'):.2f}")
    print(f"F1分数: {f1_score(true_labels, pred_labels, pos_label='好瓜'):.2f}")