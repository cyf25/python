f=open("foo.txt",'w',encoding='utf-8')
f.write("hello world")
f.close()

f=open("/foo.txt",'r')
print(f.read())
f.close()