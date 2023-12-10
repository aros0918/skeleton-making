import math

#### RightShoulder
# x = -0.075
# y = 0.067
# z = 0.755
# ang = math.acos(z)/3.14*180
# ang = ang * 2 - 90
# print(ang) ### angle calc from -x axis 

# z = math.cos((ang+90)/2/180*3.14)
# print(z)
# w = math.sqrt(1-x*x-y*y-z*z)

##### lefrShoulder
x = -0.075
y = -0.068
# z = -0.756

####### if z > -0.86
ang = math.acos(z)/3.14*180
ang = ang * 2 - 90
# print(ang) ###
z = math.cos((ang+90)/2/180*3.14)
w = math.sqrt(1-x*x-y*y-z*z)
### angle > 210 : z * -1
ang = 240
# ang = ang * 2 - 90
z = math.cos((ang+90)/2/180*3.14)
x = x
y = y
w = math.sqrt(1-x*x-y*y-z*z)
print(z)

print(1-2*(y*y+z*z)) #xx
print(2*(x*y - z*w)) #xy
print(2*(x*z+y*w)) #xz
print(2*(x*y+z*w)) #yx
print(1-2*(x*x+z*z)) #yy
print(2*(y*z-x*w))  #yz
print(2*(x*z-y*w)) #zx
print(2*(y*z+x*w)) #zy
print(1-2*(x*x+y*y)) #zz
