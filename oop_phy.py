import numpy as np
import time
import cv2 as cv
class body():
    def __init__(self, m, pos, vel, step):
        #self.rad = 0
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
        #if (maxx-minx) <= self.rad:
        #    bo = True
        a = 0
        if (maxx-minx) != 0:
            a = dm/(maxx-minx)**2*mul
        vex += a*st
        mx += vex

        mul2 = 1
        if my == maxy:
            mul2 = -1
        #if (maxy-miny) <= self.rad:
        #    bo = True
        a = 0
        if (maxy-miny) != 0:
            a = dm/(maxy-miny)**2*mul2
        vey += a*st
        my += vey

        self.x = mx
        self.xv = vex
        self.y = my
        self.yv = vey
        #return mx, my, bo

    def draw(self, co, path, col, mul):
        px, py = self.x, self.y
        if co%1 == 0:
            hx, hy = path.shape[1]/2 + px*mul, path.shape[0]/2 + py*mul
            #print(px, py)
            cv.circle(path, (int(hx), int(hy)), 1, col)

        if co%100 == 0:
            img = path.copy()
            hx, hy = path.shape[1]/2 + px*mul, path.shape[0]/2 + py*mul
            cv.circle(img, (int(hx), int(hy)), 10, col, -1)
            cv.imshow("img",img)

        return path


step=1*10**1
tt = [body(1, (-20*10**0, 0), (0,0), step),
     body(10, (20*10**0, 0), (0,0), step)]
a = tt[0]
b = tt[1]
a.pr()
b.pr()

co = 0
mul = 10
path = np.zeros((720, 1000, 3))
while 1:
    a.main(b)
    b.main(a)
    path = a.draw(co, path, (0,0,255), mul)
    path = b.draw(co, path, (0,255,0), mul)
    if co%100 == 0:
        if cv.waitKey(1) & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break

    #print(som,so2)
    #if co%1 == 0:
    #    cv.circle(path, (int(som[0]*mul)+path.shape[0]//2, int(som[1]*mul)+path.shape[1]//2), 1, (255,0,0), -1)
    #    cv.circle(path, (int(som[0]*mul)+path.shape[0]//2, int(som[1]*mul)+path.shape[1]//2), 1, (0,255,0), -1)
    #if co%100 == 0:
    #    img = path.copy()
    #    cv.circle(img, (int(som[0]*mul)+path.shape[0]//2, int(som[1]*mul)+path.shape[1]//2), 7, (255,0,0), -1)  # int(a.m*mul2)
    #    cv.circle(img, (int(som[0]*mul)+path.shape[0]//2, int(som[1]*mul)+path.shape[1]//2), 7, (0,255,0), -1)
    #    cv.imshow("img",img)
    #    if cv.waitKey(1) & 0xFF == ord('2'):
    #        cv.destroyAllWindows()
    #        break
    #if som[-1] is True or so2[-1] is True:
        #print(som[0],so2[0])
        #break
    co += 1
#print(co*a.step)
#print(time.time()-st)

#fo = (mm*dm)/(maxx-minx)**2
#fo = (6.6743015*10**-11*mm*dm)/(maxx-minx)**2
#a += (f/mm)*mul