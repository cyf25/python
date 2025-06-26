# #栈
# stack=[]
# for i in range(5):
#     stack.append(i)
# print(stack)
# print(stack.pop())#出栈
# print(stack)
# is_empty=len(stack)==0#判断是否为空
# print(is_empty)
class Stack:
    def __init__(self):
        self.stack=[]
    def push(self,item):
        self.stack.append(item)
    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            return None
    def is_empty(self):
        return self.stack==[]
    def size (self):
        return len(self.stack)
    def dayin(self):
        print(self.stack)
stack1=Stack()
stack1.push(1)
stack1.push(2)
stack1.push(3)
print(stack1.size())
print(stack1.pop())
stack1.dayin()
#队列
from collections import deque
# queue=deque()
# for i in range(5):
#     queue.append(i)
# print(queue)
class Queue:
    def __init__(self):
        self.queue=deque()
    def enqueue(self,item):
        self.queue.append(item)
    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None
    def is_empty(self):
        return self.queue==0
    def size(self):
        return len(self.queue)
    def pop(self):
        if self.queue:
            return self.queue.pop()
        else:
            return None
    def dayin(self):
        print(self.queue)
# print(queue.pop())
queue1=Queue()
queue1.enqueue(1)
queue1.enqueue(2)
queue1.enqueue(3)
queue1.enqueue(4)
queue1.enqueue(5)
print(queue1.size())
print(queue1.dequeue())
print(queue1.size())
queue1.dayin()