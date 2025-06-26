sites=["fhjashf","hjaskf","hfajksfh"]
for site in sites:
    print(site)

for i in range(5):  
    print(i)

# while循环
count = 0
while count < 5:
    print(count)
    count += 1
# break和continue
# break跳出循环
# continue跳过本次循环
for i in range(10):# 循环0-9
    if i == 5:
        break
    print(i)
for x in range(10):
    if x==5:
        continue
    print(x)
else:
    print("循环结束")
