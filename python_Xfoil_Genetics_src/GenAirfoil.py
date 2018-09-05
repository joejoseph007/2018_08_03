from BezierN import BezierN
from xfoil_dat import *

upx = [0, 0,  0.25,0.5,0.75,1]
downx = upx

upy =   [0,  0.05,    0.2,  0.15,  0.1 ,       0]
downy = [0, -0.05,   -0.1,  0.10,  0.05,       0]

n=50;
MyBezier = BezierN(6)

#=MyBesier.interpolate([0,3,2,1,0],10)
#print besierout

pupx  = MyBezier.interpolate(upx   ,n)
pupy  = MyBezier.interpolate(upy   ,n)
pdownx= MyBezier.interpolate(downx ,n)
pdowny= MyBezier.interpolate(downy ,n)

#print pupx

def savefoil(name):
    foilfile = open(name+".dat",'w')
    foilfile.write(name+"\n")
    for i in range (n,0,-1):
         foilfile.write(  " %1.6f    %1.6f\n" %(pupx[i],pupy[i]))
    for i in range (0,n+1):
         foilfile.write(  " %1.6f    %1.6f\n" %(pdownx[i],pdowny[i]))
    foilfile.close()


Re = 160000
Ncrit = 9.0

name = "testfoil"
savefoil(name)
Xfoil(name,Ncrit,Re)
print name,getLDmax(name)
