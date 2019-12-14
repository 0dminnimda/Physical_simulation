import numpy as np
import time
import pygame
from functools import reduce
import random as ra
import math as ma
from pygame.locals import *


pygame.init()

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
    f = ve_l(r)**1
    k = ve_l(r)/f
    r[0] = r[0]/k*step
    r[1] = r[1]/k*step
    return r

# класс физического тела
class body():
    def __init__(self, m, pos, vec, step, col, r, r_path, dr, react, model=0):
        self.rad = 1*10**-1 # радиус тела
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
            vec = self.vec
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

            if type != 1 and ve_l(vec) != 0:
                vve = add_vec(vec_mul(vec, 10**4.9375), (hx, hy))
                for i in range(-1, 2):
                    pygame.draw.aaline(path, (0, 255, 0), (hx, hy+i), sum_vec(vve, [0, i]), -1)
                #pygame.draw.line(path, (0, 255, 0), (hx, hy), vve, 3)

        return path

# шаг времени
step = 1*10**-6.75

# масштаб
scax = scay = 50
# сдвиг, в % от всего изображения
indx, indy = 0, 0 # percent

# реагирует ли тело на другие тела
react1 = 1
react2 = 0
react3 = 1
react4 = 1

# положение тел
xp1, yp1 = 5, 0 #ra.randint(-3, 3), ra.randint(-3, 3)#  -2.5
xp2, yp2 = 0, 0 #ra.randint(-3, 3), ra.randint(-3, 3)#
xp3, yp3 = 4, -4 #ra.randint(-3, 3), ra.randint(-3, 3)#
xp4, yp4 = -4, -4 #ra.randint(-3, 3), ra.randint(-3, 3)#

# нач скорость
xv1, yv1 = 0, 3 #ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4   5.3153
xv2, yv2 = 0 ,0 #ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
xv3, yv3 = ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4
xv4, yv4 = ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4

# масса
m1 = 1 #ra.randint(3, 7)
m2 = 10 #ra.randint(3, 7)
m3 = ra.randint(3, 7)
m4 = ra.randint(3, 7)

# цвет тел
col1 = (0, 0, 255)
col2 = (255, 0, 0)
col3 = (255, 255, 0)
col4 = (255, 255, 255)

# радиус отрисовки тел
r1 = r2 = r3 = r4 = 10

# радиус пути
rpath = 1

# отрисовка тел
draw1 = 1
draw2 = 1
draw3 = 1
draw4 = 1

star = pygame.image.load('star2.png')  #.convert()
s = 50
star = pygame.transform.scale(star, (s, s))
star.set_colorkey((255, 255, 255))


# создание экземпляра класса
a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1)
b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2, star)
c = body(m3, [xp3, yp3], [xv3, yv3], step, col3, r3, rpath, draw3, react3)
d = body(m4, [xp4, yp4], [xv4, yv4], step, col4, r4, rpath, draw4, react4)

# массив со всеми телами, что
# будут использоваться в симуляции
abod = [a, b]

# печать всех значений self для всех тел
for i in abod:
    i.pr()

# шаг
co = 0

f1 = pygame.font.SysFont("arial", 20)


bgr = pygame.image.load('space.jpeg')
#bgr = bgr.convert()
path = pygame.display.set_mode((1540, 801), RESIZABLE)  # FULLSCREEN) .convert() , SRCALPHA
#path.set_alpha(100)
bgr = pygame.transform.scale(bgr, (1540, 801))
path.blit(bgr,(0,0))
pygame.display.set_caption("Press [Space] to play/pause, [r] to reset and [esc] to escape")
rect = (0, 0)#pygame.Rect((0, path.get_height()-35))
bla = pygame.Surface((215, 25))


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
            elif event.key == K_c:
                path.blit(bgr,(0,0))
            elif event.key == K_a:
                yv1 += 1/2
                a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1)
                b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2, star)
                abod = [a, b]
            elif event.key == K_d:
                yv1 -= 1/2
                a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1)
                b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2, star)
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
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        run = False
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
    if co%100 == 0:
        # текст на изображении
        bla.fill((0, 0, 0))
        path.blit(bla, rect)
        some = ma.sqrt(ve_l([ve_l([abod[0].x, abod[1].x]), ve_l([abod[0].y, abod[1].y])]))
        text1 = f1.render(str(some), 1, (0, 0, 255))
        path.blit(text1, (0, 0))

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