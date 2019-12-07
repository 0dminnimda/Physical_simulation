import numpy as np
import time
import cv2 as cv
class body():
    def __init__(self, pos, vel, m, step):
        self.rad = 1*10**-2
        self.x, self.y = pos
        self.xv, self.yv = vel
        self.m = m
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
        mm, dm = self.m, ob.m
        mpo, dpo = self.x, ob.x
        mve, dve = self.xv, ob.xv
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
        elif (maxp-minp)**2 != 0:
            fo = (mm*dm)/(maxp-minp)**2
            #fo = (6.6743015*10**-11*mm*dm)/(maxp-minp)**2
        a = (fo/mm)*mul
        mve += a*st
        mpo += mve*st

        self.x = mpo
        self.xv = mve
        return self.x, self.xv, bo

step=1*10**2
a = [body((-1*10**0, 0), (0,0), 1*10**-10, step),
     body((1*10**0, 0), (0,0), 2*10**-10, step),
     body((1*10**0, 0), (0,0), 2*10**-10, step)]

#a.pr("x",end=" ")
#b.pr("x")
co = 0
at = 6
#st = time.time()
while 1:
    #for i in a:
    som = a[0].main(a[1])
    so2 = a[1].main(a[0])

    if co%1 == 0:
        #print(co//5000,som[3],so2[3])
        img = np.zeros((500, 500, 3))
        #img[:] = (255,255,255)
        cv.circle(img, (int(som[0]*10**2)+img.shape[1]//2,img.shape[0]//2), a.m*10, (255,0,0), -2)
        cv.circle(img, (int(so2[0]*10**2)+img.shape[1]//2,img.shape[0]//2), a.m*10, (0,255,0), -2)
        cv.imshow("img",img)
        if cv.waitKey(1) & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break
    if som[-1] is True or so2[-1] is True:
        print(som[0],so2[0])
        break
    co += 1
print(co*a.step)
#print(time.time()-st)
