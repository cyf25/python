class Student():
    def __init__(self,name,age,gender,mobile,des):
        self.name = name
        self.age=age
        self.gender=gender
        self.mobile=mobile
        self.des=des

    def __str__(self):
        return '姓名：{}，年龄：{}，性别：{}，电话：{}，描述：{}'.format(self.name,self.age,self.gender,self.mobile,self.des)
   
if __name__=='__main__':
    s1=Student('tom',18,'男','123456789','学生')
    print(s1)
    print(s1.__dict__)