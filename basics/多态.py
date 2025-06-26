class animal:
    def speak(self):
        print("animal speak")
class cat(animal):
    def speak(self):
        print("cat speak")
class dog (animal):
    def speak(self):
        print("dog speak")
def  make_speak(Animal:animal):
    Animal.speak()
cat1=cat()
dog1=dog()
Animal=animal()
make_speak(cat1)
make_speak(dog1)
make_speak(Animal)
#多态：同一个接口，不同的实现
#接口：函数或者方法