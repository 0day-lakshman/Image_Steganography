import cv2
import os
import string

img = cv2.imread("image.jpg") # Image Name or Image Path

msg = input("Enter The Secret Message : ")
password = input("Enter Passcode : ")

d = {}
c = {}

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

m = 0
n = 0
z = 0

for i in range(len(msg)):
    img[n, m, z] = d[msg[i]]
    n = n + 1
    m = m + 1
    z = (z + 1) % 3

cv2.imwrite("encryptedImage.jpg", img)
os.system("start encryptedImage.jpg")  

message = ""
n = 0
m = 0
z = 0

pas = input("Enter passcode For Decryption : ")
if password == pas:
    for i in range(len(msg)):
        message = message + c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    print("Decryption Message : ", message)
else:
    print("YOU ARE NOT An Authenticated Person!!")
