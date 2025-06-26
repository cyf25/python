class  Student:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def __str__(self):
        print('name is %s,age is %d'%(self.name,self.age))
student1=Student('tom',18)
student1.__str__()
