class AC(object):
    def cool_wind(self):
        pass
    def hot_wind(self):
        pass
    def swing_wind(self):
        pass
class geli(AC):
    def cool_wind(self):
        print('格力空调制冷')
    def hot_wind(self):
        print('格力空调制热')
    def swing_wind(self):   
        print('格力空调摆风')
class haier(AC):
    def cool_wind(self):
        print('海尔空调制冷')
    def hot_wind(self):
        print('海尔空调制热')
    def swing_wind(self):   
        print('海尔空调摆风')
class tcl(AC):
    def cool_wind(self):
        print('TCL空调制冷')
    def hot_wind(self):
        print('TCL空调制热')
    def swing_wind(self):   
        print('TCL空调摆风')
def make_wind(ac:AC):
    ac.cool_wind()
    ac.hot_wind()
    ac.swing_wind()
ac1=geli()
ac2=haier()
ac3=tcl()
make_wind(ac1)
make_wind(ac2)
make_wind(ac3)
#接口
