class car:
    def __init__(self,name,price):
        self.name = name
        self.price = price
    def __str__(self):
        return '汽车的名字是%s,价格为%d'%(self.name,self.price)
    def run(self):

        print('汽车在跑')
    def stop(self):
        self.run()
        print('汽车停了')
car1=car('奔驰',100000)
car1.run()
print(car1.name)
print(car1.price)
print(car1)