import numpy as np
from numba import jit
from random import randint

@jit(parallel=True)
def generate_sprite(radius=0,surface_radius=0,sprite=np.array,color=(0,0,0,0)):
    ''' returns a square numpy array of pixel values
        the object is depicted as two noisy grandient filled concentric circles
        the outer most of which is tangent to the square
    '''
    sprite=sprite
    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            scale=((i-radius)**2+(j-radius)**2)**0.5/radius
            scale=(scale**5)*(randint(-10,10)+100)/100
            if scale >= 1:
                continue
            else:
                for k in range(3):
                    if scale < surface_radius/radius:
                        sprite[i,j,k]=round(int(color[k]-color[k]*scale*randint(40,90)/100))
                    else:
                        sprite[i,j,k]=round(int(color[k]-color[k]*scale))
    return sprite
