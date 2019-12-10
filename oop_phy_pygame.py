import numpy as np
import time
import pygame
from functools import reduce
import random as ra
import math as ma

# сложение друх векторов
def add_vec(v, w):
    return [vi + wi for vi, wi in zip(v, w)]

# сложение нескольких векторов
def sum_vec(*vecs):
    return reduce(add_vec, vecs)

# вычисл модуля вектора
def ve_l(a):
    return np.linalg.norm(a)

# вычисл вект скорости напрпр к др телу
def v_vec(r, m, step):
    k = ve_l(r)**3/m
    r[0] = r[0]/k*step
    r[1] = r[1]/k*step
    return r

# класс физического тела
class body():
    def __init__(self, m, pos, vec, step):
        self.rad = 4*10**-1 # радиус тела
        self.m = m # масса
        self.x, self.y = pos # положение (x,y)
        self.vec = vec # вектор {x,y}
        self.step=step # шаг времени

    # печать значений объекта класса
    def pr(self,*ar,**kw):
        en = "\n"
        if kw.get("end") != None:
            en = kw.get("end")
        if len(ar) == 1:
            print(self.__dict__[ar[0]], end=en)
        else:
            print(self.__dict__, end=en)

    # просчёт физ взаимодействия
    def calc(self, *obb):
        for ob in obb:
            mx, my = self.x, self.y
            dx, dy = ob.x, ob.y
            rad = self.rad
            # если центры масс тел ближе чем
            # радиусы тел они не перестают
            # притягивать друг друга
            if (ma.fabs(mx-dx) > rad or ma.fabs(my-dy) > rad):
                # вект скорости, вызванный ускор
                # или же силой другого тела
                add_vec = v_vec([-mx+dx, -my+dy], ob.m, self.step)
                # сложение нового и старого вект
                self.vec = sum_vec(add_vec, self.vec)

        # перемещ тела на нов вектор скорости
        vec = self.vec
        self.x += vec[0]
        self.y += vec[1]

    # отрисовка положения тела
    def draw(self, path, col, r, scax, scay, indentx, indenty):
        # получение разрешения окна
        w, h = path.get_width(), path.get_height()
        px, py = self.x, self.y
        # положение центра фигуры
        hx = w/2 + px*scax + w*indentx/100
        hy = h/2 + py*scay + h*indenty/100
        pygame.draw.circle(path, col, (int(hx), int(hy)), r, r)
        return path

# шаг времени
step = 1*10**-7

# положение тел
xp1, yp1 = 4, 4
xp2, yp2 = -4, 4
xp3, yp3 = 4, -4
xp4, yp4 = -4, -4

# нач скорость
xv1, yv1 = ra.randint(-3,3)*10**-4, ra.randint(-3,3)*10**-4
xv2, yv2 = ra.randint(-3,3)*10**-4, ra.randint(-3,3)*10**-4
xv3, yv3 = ra.randint(-3,3)*10**-4, ra.randint(-3,3)*10**-4
xv4, yv4 = ra.randint(-3,3)*10**-4, ra.randint(-3,3)*10**-4

# масса
m1 = ra.randint(3,7)
m2 = ra.randint(3,7)
m3 = ra.randint(3,7)
m4 = ra.randint(3,7)

# создание экземпляра класса
a = body(m1, [xp1, yp1], [xv1, yv1], step)
b = body(m2, [xp2, yp2], [xv2, yv2], step)
c = body(m3, [xp3, yp3], [xv3, yv3], step)
d = body(m4, [xp4, yp4], [xv4, yv4], step)

# печать всех значений self
a.pr()
b.pr()
c.pr()
d.pr()

# радиус тела при отображении
r = 1
# масштаб
scax = scay = 20
# сдвиг, в % от всего изображения
indx, indy = 0, 0 # percent
# шаг
co = 0
pygame.init()
path = pygame.display.set_mode((1500, 750))
pygame.display.set_caption("Physical simulation")

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    # симуляция взаимействия
    # на тело _ действуют тела (_, _ ... _, _)
    # и оно реагирует ( движется или стоит)
    a.calc(b, c, d)
    b.calc(a, c, d)
    c.calc(a, b, d)
    d.calc(a, b, d)

    # раз в _ шагов отображаются все тела
    if co%50 == 0:
        path = a.draw(path, (0,0,255), r, scax, scay, indx, indy)
        path = b.draw(path, (255,0,0), r, scax, scay, indx, indy)
        path = c.draw(path, (0,255,0), r, scax, scay, indx, indy)
        path = d.draw(path, (255,255,0), r, scax, scay, indx, indy)

        pygame.display.update()
        # path.fill((0,0,0))

    # добавление шага
    co += 1
