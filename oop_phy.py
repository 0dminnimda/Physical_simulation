import numpy as np
import time
import cv2 as cv
class body():
    def __init__(self, pos, vel, m, step):
        self.rad = 1.6
        self.x, self.y = pos
        self.xv, self.yv = vel
        self.m = m*10**-5
        #self.g=6.6743015*10**-11
        self.step=step

    def pr(self,*ar,**kw):
        en = "\n"
        if kw.get("end") != None:
            en = kw.get("end")
        if len(ar) == 1:
            print(self.__dict__[ar[0]], end=en)
        else:
            print(self.__dict__, end=en)

    def main(self, ob):
        dm = ob.m
        mpo, dpo = self.x, ob.x
        mve = self.xv
        st = self.step
        fo = 0
        bo = False
        ar2 = np.array([mpo, dpo])
        minp, maxp = ar2.min(), ar2.max()

        mul = 1
        if mpo == maxp:
            mul = -1

        if (maxp-minp) < self.rad:
            bo = True
            a = 0
            mve = 0
        elif (maxp-minp)**2 != 0:
            a = dm/(maxp-minp)**2*mul
            mve += a*st
        
        mpo += mve

        self.x = mpo
        self.xv = mve
        return self.x, self.xv, bo


step=1*10**1
tt = [body((-20*10**0, 0), (0,0), 1, step),
     body((20*10**0, 0), (0,0), 10, step)]
a = tt[0]
b = tt[1]

co = 0
mul = 10
path = np.zeros((720, 1000, 3))
while 1:
    som = a.main(b)
    so2 = b.main(a)
    cv.circle(path, (int(som[0]*mul)+path.shape[1]//2,path.shape[0]//2), 1, (255,0,0), -1)
    cv.circle(path, (int(so2[0]*mul)+path.shape[1]//2,path.shape[0]//2), 1, (0,255,0), -1)
    if co%100 == 0:
        img = path.copy()
        cv.circle(img, (int(som[0]*mul)+img.shape[1]//2,img.shape[0]//2), 7, (255,0,0), -2)  # int(a.m*mul2)
        cv.circle(img, (int(so2[0]*mul)+img.shape[1]//2,img.shape[0]//2), 7, (0,255,0), -2)
        cv.imshow("img",img)
        if cv.waitKey(1) & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break
    #if som[-1] is True or so2[-1] is True:
        #print(som[0],so2[0])
        #break
    co += 1
#print(co*a.step)
#print(time.time()-st)

#fo = (mm*dm)/(maxp-minp)**2
#fo = (6.6743015*10**-11*mm*dm)/(maxp-minp)**2
#a += (f/mm)*mul