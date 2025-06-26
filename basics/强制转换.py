float1 =1.32875893
int1 =10
st1='10'
st2='10.0'
st3='11.23'
print(int(float1))
print(int(st1))
# print(int(st3)) #ValueError: invalid literal for int() with base 10: '11.23'string类型转为int类型，string中必须为整数，否则报错
#TypeError: 'float' object is not callable 
# print(float(st2))
print(float(int1))
print(float(st2)) 
eval(st2)
print(eval(st2))
print(type(eval(st2)))
#eval函数，将字符串中的内容作为python代码执行，并返回执行结果，除去引号，中间是什么就运行什么

