
#Genetic Algorithm visualization
from math import sin
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

def fun(x, y):
    ans = x*sin(4*x) + 1.1*y*sin(2*y)
    return ans

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = y = np.arange(-10.0, 3.0, 0.05)
X, Y = np.meshgrid(x, y)
zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)

ax.plot_surface(X, Y, Z)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()