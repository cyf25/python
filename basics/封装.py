class p():
    def __init__(self):
        self.name="张三"
        self._ID="123456789"
        self.__age=18
    def get_age(self):
         return self.__age
    def set_age(self,age):
        if age>0 and age<150:
            self._self.__age=age
        else:
            print("年龄不合法")
    def __dayin(self):
        print("我是私有方法")
    def get_dayin(self):
        self.__dayin()
class test(p):
    pass
test1=test()
print(test1.name)
print(test1.get_age())
print(test1.get_dayin())