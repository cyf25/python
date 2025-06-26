import math
import random
# print('请输入年龄') 
# age = int(input())

# if age < 18:    
#     print('未成年')
# elif age >= 18 and age < 60:
#     print('成年')
# else:   
#     print('老年')
# print('程序结束')
# print('------------------------')
# print('请输入成绩')
# score = int(input())
# if score >=90:
#     print('优秀')
# elif score >=80:
#     print('良好')
# elif score >=70:
#     print('中等')
# elif score >=60:
#     print('及格')
# else:
#     print('不及格')
# print('程序结束')
#!/usr/bin/python3
 
a = "Hello"
b = "Python"
print(f'a + b 输出结果{a} {b}')
print("a + b 输出结果：", a + b)
print("a * 2 输出结果：", a * 2)
print("a[1] 输出结果：", a[1])
print("a[1:4] 输出结果：", a[1:4])
 
if( "H" in a) :
    print("H 在变量 a 中")
else :
    print("H 不在变量 a 中")
 
if( "M" not in a) :
    print("M 不在变量 a 中")
else :
    print("M 在变量 a 中")
 
print (r'\n')
print (R'\n')
if (a is b):
    print("1-a 和 b 有相同的标识符")
else:
    print("2-a 和b 有不同的标识符")
#数学函数
X=10
abs(X)#绝对值
print(math.ceil(4.1))
Y=12
# math.cmp(X,Y)
math.exp(1)#e的x次方
list=[1,2,3,4,5]
print(max(list))#最大值
print(min(list))#最小值
print(pow(2,3))#2的3次方
print(round(4.6))#四舍五入
print(math.sqrt(16))#开平方
print(math.pi)#圆周率
print(math.e)#自然常数
print(math.floor(4.9))#向下取整
print(math.log(10,10))#对数
print(random.choice(list))#随机选择
# uniform(1,10)#随机生成1-10的数
# shuffle(list)#打乱列表
# random.randint(1,10)#随机生成1-10的整数
# random.randrange(1,10)#随机生成1-10的整数
# random.random()#随机生成0-1的数
#字符串函数
str1='hello'
str2="ranoob"
print(f'str1[0]')
print(str2[1:5])
print(str1[2:])
print(str1[-1])
#转义字符
print('hello\nworld')
print("\\")
print('\'')
print("\"")
print("hello\v world")
print("hello\t world")
