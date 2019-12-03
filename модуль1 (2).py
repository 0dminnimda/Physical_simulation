import matplotlib.pyplot as plt
import numpy as np
import math as ma
import cv2 as cv
import time

def coun(some,po,vel,step):
    g,m1,m2 = some
    posx1, posx2, posy1, posy2 = po
    vel1, vel2, vely1, vely2 = vel
    forse, forse2 = 0, 0
    if posx2-posx1 != 0:
        forse = (g*m1*m2)/(posx2-posx1)**2
    if posy2-posy1 != 0:
        forse2 = (g*m1*m2)/(posy2-posy1)**2
    a1 = forse/m1
    a2 = -forse/m2
    ay1 = forse2/m1
    ay2 = -forse2/m2

    vel1 += a1*step
    vel2 += a2*step
    vely1 += ay1*step
    vely2 += ay2*step
    posx1 += vel1*step
    posx2 += vel2*step
    posy1 += vely1*step
    posy2 += vely2*step

    return (posx1, posx2, posy1, posy2), (vel1, vel2, vely1, vely2), (a1, a2, ay1, ay2), forse

def soo(arr):
    for i in arr:
        print(len(i))

m1=1*10**-3
m2=2*10**-3
#m1 = m1**-1
#m2 = m2**-1
g=6.6743015*10**-11
rx = 1*10**0
ry = 2*10**0
posx1, posx2=0, rx
posy1, posy2=0, ry
vel1, vel2= 0, 0
vely1, vely2= 0, 0
a1, a2 = 0, 0
ay1, ay2 = 0, 0
foo = 0
step=1*10**1
num1 = 0
num2 = 0
sma = 1*10**-2

arr_v1 = []
arr_v2 = []
a_px1 = []
a_px2 = []
arr_a1 = []
arr_a2 = []

a_vy1 = []
a_vy2 = []
a_py1 = []
a_py2 = []
a_ay1 = []
a_ay2 = []

arr_f =[]
b = True
po = [posx1, posx2, posy1, posy2]
vel = [vel1, vel2, vely1, vely2]
a = [a1,a2,ay1,ay2]
zer = np.zeros((200,200,3))
mid = zer.shape[0]//2, zer.shape[1]//2
while 1:
    #plt.imshow(zer)
    if num1 % 500 == 0 and b is True:
        arr_v1.append(vel[0])
        arr_v2.append(vel[1])
        a_vy1.append(vel[2])
        a_vy2.append(vel[3])
        a_px1.append(po[0])
        a_px2.append(po[1])
        a_py1.append(po[2])
        a_py2.append(po[3])
        arr_a1.append(a[0])
        arr_a2.append(a[1])
        a_ay1.append(a[2])
        a_ay2.append(a[3])
        arr_f.append(foo)
        num2 += 1
    num1 += 1
    t = coun((g,m1,m2),po,vel,step)
    po, vel, a, foo = t

    

    if 0 <= ma.fabs(po[1]-po[0]) <= sma and 0 <= ma.fabs(po[3]-po[2]) <= sma or num2 >= 1000:
        break

#soo([arr_v1,a_vy1,a_px1,arr_a2])
posx1, posx2, posy1, posy2 = po
vel1, vel2, vely1, vely2 = vel
print(f" масса 1 тела = {m1} кг")
print(f" масса 2 тела = {m2} кг\n")
print(f" изнач. расстояние {rx} метр(ов/а)")
#print(" окончательное расстояние",pos2-pos1)
#print(" разница расстояний",r-(pos2-pos1))
print(" точка столкновения ≈", (posx1+posx2)/2, "\n")
print(" кол-во шагов", num1)
print(f" величина шага {step} сек \n")
print(" часов",step*num1/3600)
print(" минут",step*num1/60)
print(" секунд",step*num1)
print()

print(" скорость 1 тела при столкнлвении ≈",vel1)
print(" скорость 2 тела при столкнлвении ≈",vel2,"\n")
size = 10
#input()
arra = np.arange(len(arr_v1))
arra = arra*500*step/(3600)

plt.subplot(4,2,2)
plt.plot(arra, a_px1, label="1 тело", linewidth=5.0)
plt.plot(arra, a_px2, label="2 тело", linewidth=5.0)
plt.title("положение тел по x оси", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("метров")

plt.subplot(4,2,1)
plt.plot(arra, arr_v1, label="1 тело", linewidth=5.0)
plt.plot(arra, arr_v2, label="2 тело", linewidth=5.0)
plt.title("скорости тел", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("метров/сек")

'''plt.subplot(3,1,3)
plt.plot(arra, arr_f, label="сила", linewidth=3.)
plt.title("сила тяготения", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("ньютон")'''

plt.subplot(4,2,4)
plt.plot(arra, np.array(a_px2)-np.array(a_px1), label="дистанция", linewidth=5.0)
plt.title("дистанция между телами по x", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("метров")

plt.subplot(4,2,3)
plt.plot(arra, arr_a1, label="1 тело", linewidth=3.)
plt.plot(arra, arr_a2, label="2 тело", linewidth=3.)
plt.title("ускорение тел по x", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("метров/сек²")

plt.subplot(4,2,6)
plt.plot(arra, a_py1, label="1 тело", linewidth=5.0)
plt.plot(arra, a_py2, label="2 тело", linewidth=5.0)
plt.title("положение тел по y оси", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("метров")

plt.subplot(4,2,5)
plt.plot(arra, a_vy1, label="1 тело", linewidth=5.0)
plt.plot(arra, a_vy2, label="2 тело", linewidth=5.0)
plt.title("скорости тел по y", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("метров/сек")

plt.subplot(4,2,7)
plt.plot(arra, a_ay1, label="1 тело", linewidth=3.)
plt.plot(arra, a_ay2, label="2 тело", linewidth=3.)
plt.title("ускорение тел по y", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("метров/сек²")

plt.subplot(4,2,8)
plt.plot(arra, np.array(a_py2)-np.array(a_py1), label="дистанция", linewidth=5.0)
plt.title("дистанция между телами по y", fontsize=size)
plt.grid(True)
plt.legend(fontsize=size)
plt.xlabel("часов")
plt.ylabel("метров")

#plt.show()

zer = np.zeros((200,200,3))
mid = zer.shape[0]//2, zer.shape[1]//2
#zer[:] = (255,255,255)
for i in range(len(arra)):
    time.sleep(0.0001)
    po = a_px1[i], a_px2[i], a_py1[i], a_py2[i]
    zer[:] = (0,0,0)
    
    cv.circle(zer, (mid[0]+int(po[0]*50),mid[1]+int(po[2]*50)), int(m1*10000), (0,0,255), 4)
    cv.circle(zer, (mid[0]+int(po[1]*50),mid[1]+int(po[3]*50)), int(m2*10000), (0,0,255), 4)
    #cv.line(zer, (mid[0]+int(po[0]*50),mid[1]+int(po[2]*50)), (mid[0]+int(po[1]*50),mid[1]+int(po[3]*50)), (0,0,255), 5)
    cv.imshow("img",zer)
    if cv.waitKey(1) & 0xFF == ord('2'):
        break
    #zer = np.zeros((200,200,3))
    #cv.circle(zer, (int(po[0]*50),int(po[2]*50)), int(m1*10000), (0,0,255), 4)
    #cv.circle(zer, (int(po[1]*50),int(po[3]*50)), int(m2*10000), (0,0,255), 4)
    #cv.imshow("img",zer)
    #if cv.waitKey(1) & 0xFF == ord('2'):
    #    break
