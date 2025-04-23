#闭包
#1嵌套2.内部函数引用外部函数的变量 3.返回内部函数
def func_out(num1):
    def func_in(num2):
        return num1 + num2
    return func_in

add = func_out(10)
print(add(20))
