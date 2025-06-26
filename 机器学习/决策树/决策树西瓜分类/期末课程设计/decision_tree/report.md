# 基于决策树的西瓜分类项目报告

## 1. 引言

本项目旨在使用决策树算法对"西瓜数据集3.0"进行分类，以判断一个瓜是否为"好瓜"。报告将详细描述从数据处理到模型建立、训练、评估及可视化的全过程。

## 2. 数据集

数据集包含了17个西瓜样本，每个样本有6个特征属性，以及一个目标标签（"好瓜"是或否）。特征包括：`色泽`, `根蒂`, `敲声`, `纹理`, `脐部`, `触感`。

数据首先被整理成CSV格式 (`watermelon.csv`)，便于程序读取。

## 3. 方法与过程

### 3.1 数据加载与预处理

我们使用 `pandas` 库加载数据。决策树模型不能直接处理文本类型的类别数据，因此需要将其转换为数值。我们采用 `scikit-learn` 的 `LabelEncoder` 对每一个特征列进行编码。

**关键代码：**
```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# 1. 加载数据
data = pd.read_csv('decision_tree/watermelon.csv')
data = data.drop('编号', axis=1) # '编号'列与分类无关，予以删除

# 2. 将类别特征转换为数值
data_encoded = data.copy()
label_encoders = {}
for column in data_encoded.columns:
    le = LabelEncoder()
    data_encoded[column] = le.fit_transform(data_encoded[column])
    label_encoders[column] = le
```

预处理后，目标变量"好瓜"的标签被映射为：
```
{'否': 0, '是': 1}
```
这意味着在模型中，`0` 代表"否"，`1` 代表"是"。

### 3.2 训练集与测试集划分

为了评估模型的泛化能力，我们将数据集按照7:3的比例划分为训练集和测试集。

**关键代码：**
```python
from sklearn.model_selection import train_test_split

X = data_encoded.drop('好瓜', axis=1)
y = data_encoded['好瓜']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
```
划分后，我们得到11个样本用于训练，6个样本用于测试。

### 3.3 决策树算法 (ID3)

我们选用ID3算法（在`scikit-learn`中通过设置`criterion='entropy'`来实现）来构建决策树。ID3算法的核心是**信息增益**。

- **信息熵 (Entropy)**：度量一个数据集的纯度。熵越小，数据集的纯度越高。公式为：
  \[
  \text{Ent}(D) = -\sum_{k=1}^{|\mathcal{Y}|} p_k \log_2(p_k)
  \]
  其中，$p_k$ 是数据集中第 $k$ 类样本所占的比例。

- **信息增益 (Information Gain)**：表示在得知特征A的取值后，数据集D的信息熵减少的程度。增益越大，意味着使用特征A来进行划分所获得的"纯度提升"越大。公式为：
  \[
  \text{Gain}(D, a) = \text{Ent}(D) - \sum_{v=1}^{V} \frac{|D^v|}{|D|} \text{Ent}(D^v)
  \]
ID3算法在每个节点选择信息增益最大的特征进行分裂，并递归地构建决策树。

## 4. 实现与结果

### 4.1 模型训练与评估

我们使用训练集对决策树分类器进行训练，并在测试集上评估其性能。

**关键代码：**
```python
from sklearn.tree import DecisionTreeClassifier

# 训练模型
dt_classifier = DecisionTreeClassifier(criterion='entropy', random_state=42)
dt_classifier.fit(X_train, y_train)

# 评估模型
accuracy = dt_classifier.score(X_test, y_test)
print(f"模型在测试集上的准确率: {accuracy:.2f}")
```

**结果：**
模型在测试集上的准确率为 **0.33**。

**结果分析：**
这个准确率较低。主要原因是数据集非常小（仅17个样本），导致划分后的测试集样本过少（6个）。在这种情况下，模型的评估结果具有很大的偶然性，一两个样本的错误分类就会大幅拉低准确率。为了得到更可靠的模型，需要更大规模的数据集。

### 4.2 决策树可视化

为了直观地理解模型的决策过程，我们将其可视化为一张树状图。

**要成功生成图片，您需要先安装Graphviz。**

**Graphviz 安装指南 (Windows):**
1.  访问 Graphviz 官网下载页面: [https://graphviz.org/download/](https://graphviz.org/download/)
2.  下载并安装 `.exe` 文件。
3.  **重要**: 在安装过程中，确保勾选 "Add Graphviz to the system PATH for all users" 或类似的选项，将其添加到系统环境变量中。
4.  安装完成后，您可能需要重启您的开发环境（如VS Code或命令行终端）。

安装好Graphviz后，重新运行 `decision_tree_classifier.py` 脚本，即可在 `decision_tree` 目录下找到生成的决策树图片 `decision_tree.png`。

**可视化关键代码：**
```python
from sklearn.tree import export_graphviz
import pydotplus

dot_data = export_graphviz(dt_classifier,
                                feature_names=X.columns,
                                class_names=label_encoders['好瓜'].classes_,
                                filled=True,
                                rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_png('decision_tree/decision_tree.png')
```

## 5. 总结

本项目完整地演示了使用决策树算法进行分类的流程。虽然由于数据集规模的限制，模型的准确率不尽理想，但它清晰地展示了数据处理、模型构建和评估的关键步骤。最终生成的决策树可以直观地展示出模型学到的分类规则。 