class a():
    def __init__(self):
        self.a1=1
        self.a2=2
class b(a):
    def __init__(self):
        super().__init__()
        self.b1=3
        self.b2=4
class c(b):
    def __init__(self):
        super().__init__()
        self.c1=5
        self.c2=6
c1=c()
print(c1.a1)#继承父类的属性时，要手动继承super(.__init__(self))
