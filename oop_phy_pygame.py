import numpy as np
import time
import pygame
from functools import reduce
import random as ra
from random import randint as ri
import math as ma
from pygame.locals import *


# инициализация pygame
pygame.init()

# сложение друх векторов
def add_vec(v, w, sign=1):
    return [vi + wi*sign for vi, wi in zip(v, w)]

# сложение нескольких векторов
def sum_vec(*vecs):
    return reduce(add_vec, vecs)

# вычисл модуля вектора
def ve_l(a):
    return np.linalg.norm(a)

# умножение модуля
def vec_mul(arr, mul):
    return [i*mul for i in arr]

# конвертация позиций нажатий в нужные значения
def mp(sx, sy, scr, indx, indy): 
    mp = pygame.mouse.get_pos()
    x = mp[0] - scr[0]/2 - scr[0]*indx/100
    y = mp[1] - scr[1]/2 - scr[1]*indy/100
    x /= sx
    y /= sy
    return (x,y)

# вычисл вект скорости напрпр к др телу
def v_vec(r, m1, m2, step):
    dist = ve_l(r)
    f = m1*m2/dist**2
    #dist**2/m1*m2
    a = f/m1
    k = dist/a
    r[0] = r[0]/k*step
    r[1] = r[1]/k*step
    return r

# пауза
def pau():
    while 1:
        event = pygame.event.wait()
        if event.type == KEYDOWN and event.key == K_SPACE:
            return True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return False

# проверка на существование
def check(arr):
    bo = False
    for i in range(len(arr)):
        if arr[i].live is False:
            del arr[i]
            arr.insert(i, None)
            bo = True

    for _ in range(arr.count(None)):
        arr.remove(None)

    return arr, bo

# рандомный цвет
def rand_c(min=0):
    return (ri(min,255), ri(min,255), ri(min,255))

# инверсия вокруг точки
def turn(point, center):
    x = center[0] + (center[0] - point[0])
    y = center[1] + (center[1] - point[1])
    return (x,y)

# импорт картинки, реализация экрана
def main_relise(img, scr):
    bgr = pygame.image.load(img)
    path = pygame.display.set_mode(scr, RESIZABLE)  # FULLSCREEN) , SRCALPHA  path.set_alpha(100)
    bgr = pygame.transform.scale(bgr, scr)
    path.blit(bgr,(0,0))
    pygame.display.set_caption("Press [Space] to play/pause and [esc] to escape")
    return path, bgr

# импорт картинки
def img_imp(img, size=None, alpha=None):
    star = pygame.image.load(img)
    if size != None:
        star = pygame.transform.scale(star, (size, size))
    if alpha != None:
        star.set_colorkey(alpha)
    return star

# реализация текста
def font_rel(f_siz, num_symol, fram_r, fram_c, txt_font="arial"):
    font = pygame.font.SysFont(txt_font, f_siz)
    siz = (f_siz*0.65*num_symol, f_siz)
    bla = pygame.Surface(siz)
    bla.fill((0, 0, 0))
    pygame.draw.rect(bla, fram_c, (1,1, *sum_vec(siz, [-2,-2])), fram_r)
    black = bla.copy()
    return font, bla, black

# класс физического тела
class body():
    def __init__(self, m, pos, vec, step, col, r, r_path, dr, react, react2, dr_vec, bor, model=0):
        self.rad = 1*10**-5  # радиус тела
        self.borderx, self.bordery = bor  # границы
        self.live = True  # существование
        self.m = m  # масса
        self.x, self.y = pos  # положение (x,y)
        self.vec = vec_mul(vec,10**-4.5)  # вектор {x,y}
        self.step = step  # шаг времени
        self.col = col  # цвет отображения тел
        self.r_path = r_path  # радиус отрисовки тел
        self.r = r  # радиус отрисовки тел
        self.dr_bo = bool(dr)  # рисовать ли тело
        self.react = bool(react)  # реагирует ли тело на другие тела
        self.react_all = bool(react2)  # реагируют ли другие тела на тело 
        self.dr_vec = bool(dr_vec)  # рисовать ли вектор
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
            if (ma.fabs(mx-dx) > rad or ma.fabs(my-dy) > rad) and self.react is True and ob.react_all is True:
                # вект скорости, вызванный ускор
                # или же силой другого тела
                add_vec = v_vec([-mx+dx, -my+dy], self.m, ob.m, self.step)
                # сложение нового и старого вект
                self.vec = sum_vec(add_vec, self.vec)

        # перемещ тела на нов вектор скорости
        vec = self.vec
        self.x += vec[0]
        self.y += vec[1]

        bx, by = self.borderx, self.bordery

        if (bx and by) > 0:
            if ma.fabs(self.x) >= bx or ma.fabs(self.y) >= by:
                self.live = False

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

            if type != 1 and ve_l(vec) != 0 and self.dr_vec is True:
                vve = add_vec(vec_mul(vec, 10**4.9375), (hx, hy))
                #for i in range(-1, 2):
                #    pygame.draw.aaline(path, (0, 255, 0), (hx+i, hy+i), sum_vec(vve, [0+i, i]), -1)
                pygame.draw.line(path, (0, 255, 0), (hx, hy), vve, 3)

        return path

# шаг времени
step = 1*10**-6.75

# масштаб
p = 1.91
scax = scay = 50  #40*p#87.5*p

# сдвиг, в % от всего изображения
indx, indy = 0, 0 # percent

# границы
bor = (0, 0) #(16, 8)

# реагирует ли тело на другие тела
react1 = 1
react2 = 1 #

# реагируют ли другие тела на тело 
reall1 = 1
reall2 = 1

# положение тел
xp1, yp1 = 0, 0 #ra.randint(-3, 3), ra.randint(-3, 3)  -2.5
xp2, yp2 = 0, 3 #ra.randint(-3, 3), ra.randint(-3, 3)

# нач скорость
xv1, yv1 = 0, 0 #ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4   5.3153
xv2, yv2 = 4, 0 #ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4

# масса
m1 = -1 #ra.randint(3, 7)
m2 = 1*10**0.5 #ra.randint(3, 7)

# цвет тел
col1 = (0, 0, 255)
col2 = (255, 0, 0)

# частота отрисовки
dr_fr_path = 1 #+ 4*52
dr_fr_bod = 300

# радиус отрисовки тел
r1 = r2 = r3 = r4 = r_n = 10

# радиус пути
rpath = 1

# толщина линии вектора нач скорости
# при создании нового тела
st_vec_r = 6

# отрисовка тел
draw1 = 1
draw2 = 1 #
draw_n = 1

# отрисовка векторов
dr_vec1 = 1 #
dr_vec2 = 1
dr_vec_n = 1

# импорт картинки, реализация экрана
scr = (1540, 801)  #(1080, 2340)
path, bgr = main_relise("space2.jpg", scr)

star = img_imp("star2.png", 50, (255, 255, 255))

# реализация текста
dr_txt = bool( 1 )
f_siz = 75
num_symol = 6
st_point = (50, 50)
fram_c = (127, 127, 127)
font, bla, black = font_rel(f_siz, num_symol, 1, fram_c)

# параметры для шоу частота отрисовки
cha = False
conv_n = [True for _ in range(3)]
end_n = [True for _ in range(2)]
conv_v = 5.125
end_v = 20.5
i_conv = i_end = end_in = 0

# нажатие
touched = False
fr_toch = True
vec_n = [0,0]
pos_n = [0,0]

# создание экземпляра класса
a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1, reall1, dr_vec1, bor)
b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2, reall2, dr_vec2, bor,  model=star)

# массив со всеми телами, что
# будут использоваться в симуляции
abod = [a,b]

# печать всех значений self для всех тел
for i in abod:
    i.pr()

run = True
pause = False
run = pau()

# счётчик
co = 0

while run:
    # условия окончания программы
    for event in pygame.event.get():
        # нажатия мышью / пальцем
        if event.type == pygame.MOUSEBUTTONDOWN:
            touched = True
        elif event.type == pygame.MOUSEBUTTONUP:
            touched = False

        # нажатие клавиатуры
        if event.type == KEYDOWN:
            # выход
            if event.key == K_ESCAPE:
                run = False
            # очистка экрана
            elif event.key == K_c:
                path.blit(bgr,(0,0))

            # ускороние
            elif event.key == K_a:
                yv1 += 1/20
                a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1)
                b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2, star)
                abod = [a, b]
            elif event.key == K_d:
                yv1 -= 1/20
                a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1)
                b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2, star)
                abod = [a, b]

            # масштаб
            elif event.key == K_z:
                scax -= 10
                scay -= 10
            elif event.key == K_x:
                scax += 10
                scay += 10

            # частота отрисовки
            elif event.key == K_o:
                dr_fr_path += 1
            elif event.key == K_p:
                dr_fr_path -= 1

            # вывод положения тел в консоль
            elif event.key == K_f:
                for i in abod:
                    i.pr("x",end="")
                    i.pr("y")
            # пауза
            elif event.key == K_SPACE:
                #run = pau()
                pause = True

    # выполнение паузы
    if pause is True:
        run = pau()
        pause = False

    # создание нового объекта, с помощью касания
    if touched is True:
        if fr_toch is True:
            st_p_n = pygame.mouse.get_pos()
            col_n = rand_c()
            pos_n = mp(scax, scay, scr, indx, indy)
            abod.append(body(ri(1,5), pos_n, [0,0], step, col_n, r_n, rpath, draw_n, 0, 0, dr_vec_n, bor))
            fr_toch = False
    else:
        if fr_toch is False:
            vec_n = add_vec(pos_n, mp(scax, scay, scr, indx, indy), sign=-1)
            abod[-1].vec = vec_mul(vec_n, 10**-4.5)
            abod[-1].react = True
            abod[-1].react_all = True
            fr_toch = True

    # смена на следующий рисунок
    if cha is True and ve_l([abod[1].x, abod[1].y]) > end_v and end_n[i_end] is True:
        dr_fr_path += 1
        a = body(m1, [xp1, yp1], [xv1, yv1], step, col1, r1, rpath, draw1, react1, dr_vec1)
        b = body(m2, [xp2, yp2], [xv2, yv2], step, col2, r2, rpath, draw2, react2, dr_vec2, star)
        abod = [a, b]
        path.blit(bgr,(0,0))
        conv_n = [True for _ in range(3)]
        i_conv = 0
        conv_v = 5.125
        i_end = (i_end + 1)%2
        end_n[0] = end_n[1]
        end_n[1] = True
        end_in += 1

    # смена частота отрисовки
    if cha is True and ve_l([abod[1].x, abod[1].y]) > conv_v and i_conv < len(conv_n) and conv_n[i_conv] is True:
        dr_fr_path += 1
        conv_n[i_conv] = False
        conv_v += 5.125
        i_conv += 1

    abod, _ = check(abod)
    '''if bbbo is True:
        pause = True'''

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
        if co%dr_fr_path == 0:
            path = abod[i].draw(path, scax, scay, indx, indy)

    # раз в _ шагов отображаются все тела
    if co%dr_fr_bod == 0:
        # создаём копию, чтобы не повредить
        # основное изображение с путями
        img = path.copy()

        # рисуем вектор скорости нового тела
        if touched is True:
            dr_t_v = turn(pygame.mouse.get_pos(), st_p_n)
            #dr_t_v = vec_mul(dr_t_v)
            pygame.draw.line(path, col_n, st_p_n, dr_t_v, st_vec_r)

        # текст на изображении
        #bla.fill((0, 0, 0))
        if dr_txt is True:
            bla.blit(black, (0,0))
            path.blit(bla, st_point)
            some = len(abod)#ve_l([abod[1].x, abod[1].y]) #end_in 
            #ve_l([abod[0].x-abod[1].x, abod[0].y-abod[1].y])
            text1 = font.render(str(some), 1, (0, 0, 255))
            path.blit(text1, sum_vec(st_point, [5, 0]))

        for i in range(len(abod)):
            # рисуем каждое тело
            path = abod[i].draw(path, scax, scay, indx, indy, type=0)

        pygame.display.update()
        path.blit(img, (0,0))
        #path.fill((0,0,0))

    # добавление шага
    co += 1

#if __name__ == '__main__':