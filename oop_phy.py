import numpy as np
import time
class arr():
    def __init__(self, pos, vel, m):
        self.rad = 1*10**-4
        self.pos = pos
        self.vel = vel
        self.m = m
        #self.g=6.6743015*10**-11
        self.step=1*10**-3

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
        mpo, dpo = self.pos, ob.pos
        mve, dve = self.vel, ob.vel
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
            fo = (6.6743015*10**-11*mm*dm)/(maxp-minp)**2
        a = (fo/mm)*mul
        mve += a*st
        mpo += mve*st

        self.pos = mpo
        self.vel = mve
        return fo, a, self.vel, self.pos, bo

a = arr(0*10**0, 0, 1*10**-3)
b = arr(1*10**-2, 0, 2*10**-3)
a.pr("pos",end=" ")
b.pr("pos")
co = 0

st = time.time()
while 1:
    som = a.main(b)
    so2 = b.main(a)
    if co%100000 == 0:
        print(co//100000,som[3],so2[3])
    if som[-1] is True or so2[-1] is True:
        print("end", som[3],so2[3])
        break
    co += 1
print(co*a.step)
print(co*a.step/60)
print(co*a.step/3600)
print(co*a.step/(3600*24))
print(time.time()-st)
