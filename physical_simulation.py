import os


def forse(r):
    global g,m1,m2
    fo = g*m1*m2/r**2
    a1 = m1/fo
    a2 = - m2/fo
    return fo, a1, a2

def dist(pos1,pos2,vel1,vel2,step,a1, a2):
    pos1 = pos1+vel1*step+(a1*step**2)/2
    pos2 = pos2+vel2*step+(a2*step**2)/2
    vel1 += a1*step
    vel2 += a2*step

    return pos1, pos2, vel1, vel2

def coun(pos1,pos2,vel1,vel2,step):
    global g,m1,m2
    forse = (g*m1*m2)/r**2
    a1 = forse/m1
    a2 = forse/m2
    vel1 += a1*step
    vel2 += a2*step
    pos1 += vel1*step
    pos2 += vel2*step
    
    return pos1, pos2, vel1, vel2, a1, a2


m1=1*10**-3
m2=2*10**-3
#m1 = m1**-1
#m2 = m2**-1
g=6.6743015*10**-11
r = 1*10**-3
pos1, pos2=0, r
vel1, vel2=0, 0
step=1*10**-3
num1 = 0
arr_v = []
arr_p1 = []
arr_p2 = []
b = False
while 1:
    #if num1 % 500 == 0 and b is True:
    #arr_v.append([vel1,vel2])
    arr_p1.append(pos1)
    arr_p2.append(pos2)
    num1 += 1
    t = coun(pos1,pos2,vel1,vel2,step)
    pos1, pos2, vel1, vel2, a1, a2 = t

    if (pos2-pos1) <= 0:
        break

print(f" изнач. расстояние {r} метр(ов/а)")
#print(" окончательное расстояние",pos2-pos1)
#print(" разница расстояний",r-(pos2-pos1))
print(" точка столкновения ≈", pos1)#pos1+(pos2-pos1)/2,"\n")
print(" кол-во шагов", num1)
print(" часов",step*num1/3600)
print(" минут",step*num1/60)
print(" секунд",step*num1)
print()


print(" скорость 1 тела при столкнлвении",vel1)
print(" скорость 2 тела при столкнлвении",vel2,"\n")
#print(arr_v,arr_p)

f = open("text1.txt", "w")
#f.write(str(arr_v))
#f.write("\n\n\n")
for i in arr_p1:
    f.write(str(i)+" ")
f.close()
f = open("text2.txt", "w")
for i in arr_p2:
    f.write(str(i)+" ")
f.close()