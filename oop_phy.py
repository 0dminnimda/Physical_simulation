import numpy as np
import time
import cv2 as cv


class body():
    def __init__(self, m, pos, vel, v_vec, step):
        self.rad = 2
        self.x, self.y = pos
        self.xv, self.yv = vel
        self.v_vec = [self.x, self.y, self.xv, self.yv]#v_vec
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

    def m_vec(self, ob):
        def add_vectors(v, w):
            return [vi + wi for vi, wi in zip(v.copy(), w.copy())]

        def sum_of_all_vectors(vecs):
            return reduce(add_vectors, vecs)

        def ve_l(a):
            b = np.linalg.norm([a[2]-a[0], a[3]-a[1]])
            print(a,b)
            return b

        def v_vec(r, m, step):
            a = m/ve_l(r)**2
            r[2] = r[2]*a/ve_l(r)
            r[3] = r[3]*a/ve_l(r)
            return r

        def new_vec(vec, r, m, step):
            vec2 = v_vec(r, m, step)
            return add_vectors(vec, vec2)

        def move(vec):
            vec = vec.copy()
            x = max(vec[:2])-min(vec[:2])
            y = max(vec[1:])-min(vec[1:])
            vec[0] += x
            vec[2] += x
            vec[1] += y
            vec[3] += y
            #for i in range(len(vec)):
            #    if i%2==0:
            #        vec[i] += x
            #    elif i%2==1:
            #        vec[i] += y
            return vec

        vec = self.v_vec
        r = [vec[0], vec[1], ob.v_vec[0], ob.v_vec[1]]
        vec = new_vec(vec, r, ob.m, self.step)
        self.v_vec = move(vec)

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


step=1*10**-2
tt = [body(1, (10*10**0, 0), (0,-1*10**-1), [], step),
     body(1,  (0*10**0, 0), (0,0*10**-3.5), [], step)]
a = tt[0]
b = tt[1]
a.pr()
b.pr()


scax = scay = 10
co = 0
path = np.zeros((720, 1000, 3))
while 1:
    a.m_vec(b)
    b.m_vec(a)

    if co%100 == 0:
        path = a.draw(path, (0,0,255), 1, scax, scay)
        path = b.draw(path, (255,0,0), 1, scax, scay)
    
    if co%1000 == 0:
        img = a.draw(path.copy(), (0,0,255), 3, scax, scay)
        img = b.draw(img, (255,0,0), 3, scax, scay)
        cv.imshow("img", img)
        if cv.waitKey(1) & 0xFF == ord('2'):
            cv.destroyAllWindows()
            break
    co += 1

#fo = (mm*dm)/(maxx-minx)**2
#fo = (6.6743015*10**-11*mm*dm)/(maxx-minx)**2
#a += (f/mm)*mul