import numpy as np
import time
import pygame
from functools import reduce
import random as ra
import math as ma
from pygame.locals import *

# сложение друх векторов
def add_vec(v, w):
    return [vi + wi for vi, wi in zip(v, w)]

# сложение нескольких векторов
def sum_vec(*vecs):
    return reduce(add_vec, vecs)

# вычисл модуля вектора
def ve_l(a):
    return np.linalg.norm(a)

def vec_mul(arr, mul):
    return [i*mul for i in arr]

# вычисл вект скорости напрпр к др телу
def v_vec(r, m, step):
    k = ve_l(r)**3/m
    r[0] = r[0]/k*step
    r[1] = r[1]/k*step
    return r

# класс физического тела
class body():
    def __init__(self, m, pos, vec, step, col, r, r_path, dr, react, model=0):
        self.rad = 0#4*10**-1 # радиус тела
        self.m = m # масса
        self.x, self.y = pos # положение (x,y)
        self.vec = vec_mul(vec,10**-4.5) # вектор {x,y}
        self.step = step # шаг времени
        self.col = col # цвет отображения тел
        self.r_path = r_path # радиус отрисовки тел
        self.r = r # радиус отрисовки тел
        self.dr_bo = bool(dr) # рисовать ли тело
        self.react = bool(react)  # реагирует ли тело на другие тела
        self.model = model  # отрисует картинку вместо точки

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
            if (ma.fabs(mx-dx) > rad or ma.fabs(my-dy) > rad) and self.react is True:
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
    def draw(self, path, scax, scay, indentx, indenty, type=1):
        if self.dr_bo is True:
            # получение разрешения окна
            w, h = path.get_width(), path.get_height()
            px, py = self.x, self.y
            col = self.col
            if type == 1:
                r = self.r_path
                type = r
            elif type == 0:
                r = self.r

            # положение центра фигуры
            hx = w/2 + px*scax + w*indentx/100
            hy = h/2 + py*scay + h*indenty/100

            mo = self.model
            if type != 1 and mo != 0:
                path.blit(mo, (int(hx-mo.get_width()//2), int(hy-mo.get_height()//2)))
            else:
                pygame.draw.circle(path, col, (int(hx), int(hy)), r, type)

        return path

# шаг времени
step = 1*10**-6.75

# реагирует ли тело на другие тела
react1 = 1
react2 = 0

# положение тел
xp1, yp1 = -4, 0
xp2, yp2 = 0, 0
xp3, yp3 = 4, -4
xp4, yp4 = -4, -4

# нач скорость
xv1, yv1 = 0, 5  #ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
xv2, yv2 = 0, 0  #ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
xv3, yv3 = ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
xv4, yv4 = ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4

# масса
m1 = 1  #ra.randint(3, 7)
m2 = 1  #ra.randint(3, 7)
m3 = ra.randint(3, 7)
m4 = ra.randint(3, 7)

# цвет тел
col1 = (0, 0, 255)
col2 = (255, 0, 0)
col3 = (0, 255, 0)
col4 = (255, 255, 255)

# радиус отрисовки тел
r1 = r2 = r3 = r4 = 6

# радиус пути
rpath = 1

# отрисовка тел
draw1 = 1
draw2 = 1
draw3 = 1
draw4 = 1

star = pygame.image.load('star.jpg')  #.convert()

star = pygame.transform.scale(star, (50, 50))

# создание экземпляра класса
a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1)
b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2, star)
#c = body(m3, [xp3, yp3], [xv3, yv3], step, col3, r3, rpath, draw3)
#d = body(m4, [xp4, yp4], [xv4, yv4], step, col4, r4, rpath, draw4)

# массив со всеми телами, что
# будут использоваться в симуляции
abod = [a, b]

# печать всех значений self для всех тел
for i in abod:
    i.pr()

# масштаб
scax = scay = 30
# сдвиг, в % от всего изображения
indx, indy = 0, 0 # percent
# шаг
co = 0

pygame.init()
bgr = pygame.image.load('space.jpeg')
path = pygame.display.set_mode((1540, 800), RESIZABLE)  # FULLSCREEN) .convert()
bgr = pygame.transform.scale(bgr, (1540, 800))
path.blit(bgr,(0,0))
pygame.display.set_caption("Press [Space] to play/pause, [r] to reset and [esc] to escape")

run = True

while 1:
    event = pygame.event.wait()
    if event.type == KEYDOWN and event.key == K_SPACE:
        break
    elif event.type == KEYDOWN and event.key == K_ESCAPE:
        run = False
        break

while run:
    # условия окончания программы
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
            elif event.key == K_a:
                yv1 += 1
                a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1)
                b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2)
                abod = [a, b]
            elif event.key == K_d:
                yv1 -= 1
                a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1)
                b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2)
                abod = [a, b]
            #elif event.key == K_r:
            #    xv1, yv1 = ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
            #    xv2, yv2 = ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
            #    xv3, yv3 = ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
            #    xv4, yv4 = ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
            #    m1 = ra.randint(3, 7)
            #    m2 = ra.randint(3, 7)
            #    m3 = ra.randint(3, 7)
            #    m4 = ra.randint(3, 7)
            #    a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1)
            #    b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2)
            #    c = body(m3, [xp3, yp3], [xv3, yv3], step, col3, r3, rpath, draw3)
            #    d = body(m4, [xp4, yp4], [xv4, yv4], step, col4, r4, rpath, draw4)
            #    abod = [a, b, c, d]
            #    path.fill((0, 0, 0))
            elif event.key == K_SPACE:
                while 1:
                    event = pygame.event.wait()
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        break

    # цикл перечисляет все элементы
    # массива с телами
    for i in range(len(abod)):
        other = abod[:]
        del other[i]
        # симуляция взаимействия
        # на тело i действуют тела other
        # и оно реагирует ( движется или стоит)
        abod[i].calc(*other)

        # раз в _ шагов отображаются все пути тел
        if co%10 == 0:
            path = abod[i].draw(path, scax, scay, indx, indy)
    
    # раз в _ шагов отображаются все тела
    if co%250 == 0:
        # создаём копию, чтобы не повредить
        # основное изображение с путями
        img = path.copy()
        for i in range(len(abod)):
            # рисуем каждое тело
            path = abod[i].draw(path, scax, scay, indx, indy, type=0)

        pygame.display.update()
        path.blit(img, (0,0))
        #path.fill((0,0,0))

    # добавление шага
    co += 1