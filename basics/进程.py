import time
import multiprocessing
def music():
    for i in range(10):
        print(f'第{i}首music')
        time.sleep(0.2)
def conding():
    for i in range(10):
        print(f'第{i}次coding')
        time.sleep(0.2)
if __name__ == '__main__':
    t1=time.time()
    #进程
    p1=multiprocessing.Process(target=music,name='p1')#创建进程
    p2=multiprocessing.Process(target=conding,name='p2')
    p1.start()
    p2.start()
    p1.join()#主程序等待进程结束后再执行
    p2.join()#等待进程结束
    t2=time.time()
    print(f'程序执行时间{t2-t1}')
