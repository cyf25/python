list1=['good','bad','nice',1997,2000,1998]
print(list1[1])
print(list1[0:3])#到第三个元素
print(list1[1:-2])#从第二个元素到倒数第三个元素
list1.append('giegie')#在列表末尾添加元素
print(list1)
list1.insert(1,'haha')#在第一个元素前插入
del list1[0]#除第个元素
print(list1)
list1.remove('giegie')#删除指定元素
print(list1)
len(list1)#列表长度
print(list1.count(1997))#元素个数
# list1.sort()#排序
import operator
# operator.index('bad')#元素位置
print(f'相等吗？{operator.eq(list1[0],list1[1])}')
#元组,不能修改
tuple1=('good','bad','nice',1997,2000,1998)
print(tuple1[1])
print(tuple1[0:3])#到第三个元素
print(tuple1[1:-2])#从第二个元素到倒数第三个元素
type(tuple1)#类型
print(tuple1)
print(list(tuple1))
#字典 
dict1={'name':'tom' ,'age':18}
print(dict1)
print(dict1['name'])
dict1['name']='jerry'
print(dict1)
print(dict1.keys())
print(dict1.values())
print(type(dict1))
#集合
set1={1,2,3,4,5,6,7,8,9,10}
print(set1)
a=set('abajsfhjakfgjhfeuwfgiuk')
print(a)
b=set('ab')
print(a-b)#差集
print(a|b)#并集
print(a&b)#交集
print(a^b)#对称差集
#集合是无序的
#集合中的元素不能重复
#集合中的元素必须是不可变类型
c={x for x in 'abcsdfghjk' if x not in 'abc'}
#{x for ...}:
# 将满足条件的字符 x 放入一个集合中。集合的特性是元素唯一且无序
#用于从字符串 'abracadabra' 中筛选出不在字符串 'abc' 中的字符，并将这些字符存储在一个集合 a 中。
print(c)
# a={x for x in 'abasjfhkjahf' if x not in 'abc'}
b.add('good')
print(b)
b.update(tuple1)#添加多个元素,可以为元组集合列表
print(b)
b.remove('good')#删除元素
print(b)
b.discard('a')#删除元素,如果不存在则不报错
b.pop()#删除第一个元素
print(b)
len(b)#长度
r='good' in b#判断元素是否存在
print(r)

#集合是无序的