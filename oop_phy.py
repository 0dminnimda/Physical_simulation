import numpy as np
import time
import cv2 as cv
from functools import reduce


class body():
    def __init__(self, m, pos, vec, step):
        #self.rad = 2
        self.m = m#*10**-5
        self.x, self.y = pos
        self.vec = vec
        self.step=step
        #self.g=6.6743015*10**-11
        pass

    def pr(self,*ar,**kw):
        en = "\n"
        if kw.get("end") != None:
            en = kw.get("end")
        if len(ar) == 1:
            print(self.__dict__[ar[0]], end=en)
        else:
            print(self.__dict__, end=en)

    def calc(self, ob):
        def add_vec(v, w):
            return [vi + wi for vi, wi in zip(v, w)]

        def sum_vec(*vecs):
            return reduce(add_vec, vecs)

        def ve_l(a):
            return np.linalg.norm(a)

        def v_vec(r,m,step):
            k = ve_l(r)**3/m
            r[0]=r[0]/k*step
            r[1]=r[1]/k*step
            return r

        mx, my = self.x, self.y
        dx, dy = ob.x, ob.y
        nvec = v_vec([-mx+dx, -my+dy], ob.m, self.step)
        self.vec = sum_vec(nvec, self.vec)

    def move(self):
        vec = self.vec
        self.x += vec[0]
        self.y += vec[1]

    def main(self, ob):
        dm = ob.m
        mx, dx = self.x, ob.x
        my, dy = self.y, ob.y
        vex = self.xv
        vey = self.yv
        st = self.step
        fo = 0
        bo = False
        ar = [my, dy]
        ar2 = [mx, dx]
        minx, maxx = min(ar2), max(ar2)
        miny, maxy = min(ar), max(ar)

        mul = 1
        if mx == maxx:
            mul = -1
        if (maxx-minx) <= self.rad:
            bo = True
            a = 0
        elif (maxx-minx) != 0:
            a = dm/(maxx-minx)**2*mul
        vex += a*st
        mx += vex*st

        mul2 = 1
        if my == maxy:
            mul2 = -1
        if (maxy-miny) <= self.rad:
            bo = True
            a2 = 0
        elif (maxy-miny) != 0:
            a2 = dm/(maxy-miny)**2*mul2
        vey += a2*st
        my += vey*st

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


step=1*10**-6.5
#a = body(1, (10*10**0, 0), (0,-1*10**-1), [], step)
#b = body(1,  (0*10**0, 0), (0,0*10**-3.5), [], step)
a = body(1, [-2,0], [0,0], step)
b = body(1, [2,0], [0,1*10**-3.75], step)

#a.calc(b)
#a.move()

scax = scay = 20
co = 0
path = np.zeros((720, 1000, 3))
while 1:
    a.calc(b)
    a.move()
    b.calc(a)
    b.move()
    #a.m_vec(b)
    #b.m_vec(a)

    if co%100 == 0:
        path = a.draw(path, (0,0,255), 1, scax, scay)
        path = b.draw(path, (255,0,0), 1, scax, scay)
    
    if co%1000 == 0:
        img = a.draw(path.copy(), (0,0,255), 4, scax, scay)
        img = b.draw(img, (255,0,0), 4, scax, scay)
        cv.imshow("img", img)
        if cv.waitKey(1) & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break
    co += 1