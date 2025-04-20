import pandas as pd

class dataed:
    def dataed(self, data):
        """处理数据，筛选订单类型为'下单'的记录"""
        self.data = data  # 保存原始数据
        filtered_data = data[data['订单类型'] == '下单']  # 更高效的筛选方式
        return filtered_data.copy()  # 返回副本避免SettingWithCopyWarning
