class version1(object):
    def pow(self):
        return 60
class version2(version1):
    def pow(self):
        return 80
class enemy(object):
    def pow(self):
        return 70
def object_play(Version:version1,Enemy:enemy):#多态 函数
    if (Version.pow()>Enemy.pow()):
        print("我方赢了")
    else:
        print("我方输了")
Version2=version2()
Version1=version1()
print("版本1与敌人对战")
object_play(Version1,enemy())#
print("版本2与敌人对战")
object_play(Version2,enemy())

''''
''多态战机对战
'''