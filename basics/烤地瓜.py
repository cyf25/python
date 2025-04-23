class kaodigua:
    def  __init__(self):
        self._time = 0
        self.cook = '生'
        self.tiaoliao = '无'
    def __str__(self):
        return '地瓜已经烤了{}分钟，状态是{}'.format(self._time, self.cook)
    def cook_time(self, time):  # 烤地瓜
        self._time += time
        if self._time < 3:
            self.cook = '生'
        elif self._time < 5:
            self.cook = '半生不熟'
        elif self._time < 8:
            self.cook = '熟'
        else:
            self.cook = '糊了'
    def add(self, tiaoliao):
        self.tiaoliao = tiaoliao

dg1 = kaodigua()
a = int(input('地瓜烤了多长时间？'))
dg1.cook_time(a)
print(dg1)