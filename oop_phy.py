import numpy as np
import time
import cv2 as cv
from functools import reduce
import random as ra


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

    def calc(self, *obb):
        for ob in obb:
            mx, my = self.x, self.y
            dx, dy = ob.x, ob.y
            nvec = v_vec([-mx+dx, -my+dy], ob.m, self.step)
            self.vec = sum_vec(nvec, self.vec)
        vec = self.vec
        self.x += vec[0]
        self.y += vec[1]

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

    def draw(self, path, col, r, scax, scay, indentx, indenty):
        px, py = self.x, self.y
        hx = path.shape[1]/2 + px*scax + path.shape[1]*indentx/100
        hy = path.shape[0]/2 + py*scay + path.shape[0]*indenty/100
        cv.circle(path, (int(hx), int(hy)), r, col, -1)
        return path


step=1*10**-6

xp1, yp1 = 5, -3
xp2, yp2 = -5, -3
xp3, yp3 = 0, 4.5

xv1, yv1 = ra.randint(-2,2)*10**-4, ra.randint(-2,2)*10**-4
xv2, yv2 = ra.randint(-2,2)*10**-4, ra.randint(-2,2)*10**-4
xv3, yv3 = ra.randint(-2,2)*10**-4, ra.randint(-2,2)*10**-4

m1 = 5
m2 = 5
m3 = 3

a = body(m1, [xp1, yp1], [xv1, yv1], step)
b = body(m2, [xp2, yp2], [xv2, yv2], step)
c = body(m3, [xp3, yp3], [xv3, yv3], step)

scax = scay = 7.5
indx, indy = 0, 0  # percent
co = 0
path = np.zeros((790, 1300, 3))
while 1:
    a.calc(b)
    b.calc(a)
    #c.calc(a, b)

    if co%1 == 0:
        path = a.draw(path, (0,0,255), 1, scax, scay, indx, indy)
        path = b.draw(path, (255,0,0), 1, scax, scay, indx, indy)
        #path = c.draw(path, (0,255,0), 1, scax, scay, indx, indy)
    
    if co%500 == 0:
        img = a.draw(path.copy(), (0,0,255), 6, scax, scay, indx, indy)
        img = b.draw(img, (255,0,0), 6, scax, scay, indx, indy)
        #img = c.draw(img, (0,255,0), 6, scax, scay, indx, indy)
        cv.imshow("img", img)
        if cv.waitKey(1) & 0xFF == ord('2'):
            #cv.imwrite("physics_sim.png", img)
            #cv.destroyAllWindows()
            path = np.zeros((790, 1300, 3))
            #break
            xp1, yp1 = ra.randint(-7,7), ra.randint(-7,7)
            xp2, yp2 = ra.randint(-7,7), ra.randint(-7,7)
            xv1, yv1 = ra.randint(-3,3)*10**-4, ra.randint(-3,3)*10**-4
            xv2, yv2 = ra.randint(-3,3)*10**-4, ra.randint(-3,3)*10**-4
            m1 = ra.randint(1,5)
            m2 = ra.randint(1,5)
            a = body(m1, [xp1, yp1], [xv1, yv1], step)
            b = body(m2, [xp2, yp2], [xv2, yv2], step)
    co += 1
print(co)