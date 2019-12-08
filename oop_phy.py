import numpy as np
import time
import cv2 as cv


class body():
    def __init__(self, m, pos, vel, step):
        self.rad = 2
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
        mx, dx = self.x, ob.x
        my, dy = self.y, ob.y
        vex = self.xv
        vey = self.yv
        st = self.step
        fo = 0
        bo = False
        ar = np.array([my, dy])
        ar2 = np.array([mx, dx])
        minx, maxx = ar2.min(), ar2.max()
        miny, maxy = ar.min(), ar.max()

        mul = 1
        if mx == maxx:
            mul = -1
        if (maxx-minx) <= self.rad:
            bo = True
            a = 0
        elif (maxx-minx) != 0:
            a = dm/(maxx-minx)**2*mul
        vex += a*st
        mx += vex

        mul2 = 1
        if my == maxy:
            mul2 = -1
        if (maxy-miny) <= self.rad:
            bo = True
            a2 = 0
        elif (maxy-miny) != 0:
            a2 = dm/(maxy-miny)**2*mul2
        vey += a2*st
        my += vey

        self.x = mx
        self.xv = vex
        self.y = my
        self.yv = vey
        #return mx, my, bo
        pass

    def draw(self, path, col, r, scax, scay):
        px, py = self.x, self.y
        hx, hy = path.shape[1]/2 + px*scax, path.shape[0]/2 + py*scay
        cv.circle(path, (int(hx), int(hy)), r, col, -1)

        return path


step=1*10**-2
tt = [body(1, (10*10**0, 0), (0,-1*10**-4), step),
     body(0, (0*10**0, 0), (0,0*10**-3.5), step)]
a = tt[0]
b = tt[1]
a.pr()
b.pr()


scax = scay = 10
co = 0
path = np.zeros((720, 1000, 3))
while 1:
    a.main(b)
    #b.main(a)
    if co%100 == 0:
        path = a.draw(path, (0,0,255), 1, scax, scay)
        path = b.draw(path, (255,0,0), 1, scax, scay)
    
    if co%1000 == 0:
        img = a.draw(path.copy(), (0,0,255), 7, scax, scay)
        img = b.draw(img, (255,0,0), 7, scax, scay)
        cv.imshow("img", img)
        if cv.waitKey(1) & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break
    co += 1

#fo = (mm*dm)/(maxx-minx)**2
#fo = (6.6743015*10**-11*mm*dm)/(maxx-minx)**2
#a += (f/mm)*mul