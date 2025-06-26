import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import pydotplus
import collections
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号
from sklearn import tree

# 1. 加载数据
data = pd.read_csv('decision_tree/watermelon.csv')

# 2. 数据预处理
# 删除'编号'列
data = data.drop('编号', axis=1)

# 将类别特征转换为数值
# 对每一列使用独立的LabelEncoder
data_encoded = data.copy()
label_encoders = {}
for column in data_encoded.columns:
    le = LabelEncoder()
    data_encoded[column] = le.fit_transform(data_encoded[column])
    label_encoders[column] = le

# 3. 划分特征和标签
X = data_encoded.drop('好瓜', axis=1)
y = data_encoded['好瓜']
feature_names = X.columns
# 从'好瓜'列的编码器中获取类名，以确保顺序正确
class_names = label_encoders['好瓜'].classes_

# 4. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 5. 训练决策树模型
# 使用ID3算法 (信息增益)
dt_classifier = DecisionTreeClassifier(criterion='entropy', random_state=42)
dt_classifier.fit(X_train, y_train)

# 7. 评估模型
accuracy = dt_classifier.score(X_test, y_test)
print(f"模型在测试集上的准确率: {accuracy:.2f}")

# 6. 可视化决策树 (使用 Matplotlib)
print("\n正在使用 Matplotlib 生成决策树图片...")
plt.figure(figsize=(20,10))
tree.plot_tree(dt_classifier,
               feature_names=feature_names,
               class_names=class_names,
               filled=True,
               rounded=True,
               fontsize=10)
plt.savefig('decision_tree/decision_tree_matplotlib.png')
print("决策树图片已保存为 'decision_tree/decision_tree_matplotlib.png'")

# 为了报告，打印出一些计算过程
print("\n--- 训练完成 ---")
print(f"特征: {list(feature_names)}")
# 获取'好瓜'列的编码映射
good_melon_mapping = {label: index for index, label in enumerate(label_encoders['好瓜'].classes_)}
print(f"目标'好瓜'的值映射: {good_melon_mapping}")
print(f"训练集大小: {len(X_train)} samples")
print(f"测试集大小: {len(X_test)} samples")
print("决策树已生成并保存为 'decision_tree/decision_tree_matplotlib.png'") 