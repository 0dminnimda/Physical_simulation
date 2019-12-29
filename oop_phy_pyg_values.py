import numpy as np
import time
import pygame
from functools import reduce
import random as ra
from random import randint as ri
import math as ma
from pygame.locals import *
from oop_phy_pygame import *

# инициализация pygame
pygame.init()

# масштаб
p = 1.91
scax = scay = 50  #40*p#87.5*p

# сдвиг, в % от всего изображения
indx, indy = 0, 0 # percent

# масса
m1 = -1 #ra.randint(3, 7)
m2 = 1*10**0.5 #ra.randint(3, 7)

# положение тел
xp1, yp1 = 0, 0 #ra.randint(-3, 3), ra.randint(-3, 3)  -2.5
xp2, yp2 = 0, 3 #ra.randint(-3, 3), ra.randint(-3, 3)

# нач скорость
xv1, yv1 = 0, 0 #ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4   5.3153
xv2, yv2 = 4, 0 #ra.randint(-3, 3)*10**-4, ra.randint(-3, 3)*10**-4

# шаг времени
step = 1*10**-6.75

# границы
border = (0, 0) #(16, 8)

# реагирует ли тело на другие тела
react1 = 1
react2 = 1 #

# реагируют ли другие тела на тело 
reall1 = 1
reall2 = 1

# цвет тел
col1 = (0, 0, 255)
col2 = (255, 0, 0)

# радиус пути
rpath = 1

# радиус отрисовки тел
r1 = r2 = r3 = r4 = r_n = 10

# отрисовка тел
draw1 = 1
draw2 = 1 #
draw_n = 1

# максимальное количество точек в массиве пути
max = 500

# соединять ли точки пути
conn = bool( 1 )

# движение
ind_n = 0.005
ind_c = 1

#
sca_n = 0.005
sca_c = 1


# отрисовка векторов
dr_vec1 = 1 #
dr_vec2 = 1
dr_vec_n = 1

# толщина линии вектора нач скорости
# при создании нового тела
st_vec_r = 6

# частота отрисовки
dr_fr_path = 50 #+ 4*52
dr_fr_body = 300

# импорт картинки, реализация экрана
scr = (1540, 801)  #(1080, 2340)
path, bgr = main_relise("space2.jpg", scr)
star = img_imp("star2.png", 50, (255, 255, 255))

# реализация текста
dr_txt = bool( 1 )
f_siz = 30
num_symol = 6
st_point = (15, 15)
fram_c = (127, 127, 127)
font, bla, black = font_rel(f_siz, num_symol, 1, fram_c)

# параметры для шоу "смена частоты отрисовки"
cha = False
conv_n = [True for _ in range(3)]
end_n = [True for _ in range(2)]
conv_v = 5.125
end_v = 20.5
i_conv = i_end = end_in = 0

# создание экземпляра класса
a = body(m1, [xp1, yp1], [xv1, yv1], (step, border, react1, reall1), (col1, rpath, r1, draw1, dr_vec1, max, conn))
b = body(m2, [xp2, yp2], [xv2, yv2], (step, border, react2, reall2), (col2, rpath, r2, draw2, dr_vec2, max, conn), model=star)

# массив со всеми телами, что
# будут использоваться в симуляции
all_bodies = [a,b]

# создаём "упаковки" для информации
txt = dr_txt, st_point, font, bla, black
draw = scr, path, bgr, dr_fr_path, dr_fr_body, max, conn
correction = scax, scay, indx, indy, ind_n, ind_c, sca_n, sca_c
show = cha, conv_n, end_n, conv_v, end_v, i_conv
phy = step, border, rpath, r_n, draw_n, dr_vec_n, st_vec_r

main_f(all_bodies, phy, draw, txt, show, correction)
