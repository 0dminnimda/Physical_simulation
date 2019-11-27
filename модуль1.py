import cv2 as cv
import numpy as np


pos1, pos2 = [], []
f = open("text1.txt", "r")
t = f.read()
arr1 = list(t.split())
for i in range(len(arr1)):
    if i % 10**2 == 0:
        pos1.append(float(arr1[i]))
f.close()

f = open("text2.txt", "r")
t = f.read()
arr2 = list(t.split())
for i in range(len(arr2)):
    if i % 10**2 == 0:
        pos2.append(float(arr2[i]))
f.close()
print(len(arr1),len(pos1))
co = 10**5
#img = np.zeros((720//2,1280//2,3))
#print(img.shape[2]-img.shape[1]//6-int(pos2[2]*co))

for i in range(len(pos1)):
    img = np.zeros((700//2,1000//2,3))
    cv.circle(img, (int(pos1[i]*co),img.shape[1]//2),1,(0,0,255),2)
    cv.circle(img, (img.shape[1]-int(pos2[i]*co),img.shape[1]//2),2,(0,0,255),2)
    cv.imshow("some", img)
    if cv.waitKey(1) & 0xFF == ord('2'):
        break
