def cheak(fn):
    def long ():
        print('登录！')
        fn()
    return long

@cheak
def func1():
    print('评论')
func1()
