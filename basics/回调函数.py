def work01():
    print('work01')

def work02():
    print('work02')

def work03():
    print('work03')

def workfram(mycallback):
    mycallback()
    pass
#直接调用
work01()
#间接调用
workfram(work02)