'''
  File name: carv.py
  Author:
  Date created:
'''

'''
  File clarification:
    Aimed to handle finding seams of minimum energy, and seam removal, the algorithm
    shall tackle resizing images when it may be required to remove more than one seam, 
    sequentially and potentially along different directions.
    
    - INPUT I: n × m × 3 matrix representing the input image.
    - INPUT nr: the numbers of rows to be removed from the image.
    - INPUT nc: the numbers of columns to be removed from the image.
    - OUTPUT Ic: (n − nr) × (m − nc) × 3 matrix representing the carved image.
    - OUTPUT T: (nr + 1) × (nc + 1) matrix representing the transport map.
'''
import cumMinEngHor
import cumMinEngVer
import rmVerSeam
import rmHorSeam
import genEngMap
import numpy as np
import imageio
from PIL import Image
import time


def backtrack(T, y, x, image_list, gif_list, i):
  if (y == 0 and x == 0):
    gif_list[i] = image_list[0][0]
    return gif_list
  gif_list[i] = image_list[y][x]
  i = i - 1
  val = T[y, x]
  if (val == 1):
    y = y - 1
    backtrack(T, y, x, image_list, gif_list, i)
  else:
    x = x - 1
    backtrack(T, y, x, image_list, gif_list, i)
  return gif_list


def carv(I, nr, nc):
  # Your Code Here
  r = nr+1
  c = nc+1
  image_list = [[[] for j in range(c)] for i in range(r)]
  T = np.zeros((r, c))
  Tr = np.zeros((r, c))
  image_list[0][0]=np.copy(I)

  for i in list(range(1,c)):
    img = np.copy(image_list[0][i-1])
    e = genEngMap.genEngMap(img)
    M_left,Tb_left = cumMinEngVer.cumMinEngVer(e)
    image,cost=rmVerSeam.rmVerSeam(img,M_left,Tb_left)
    image_list[0][i] = np.copy(image)
    Tr[0][i] = Tr[0][i-1]+cost

  for j in list(range(1,r)):
    img = np.copy(image_list[j-1][0])
    e = genEngMap.genEngMap(img)
    M_up,Tb_up = cumMinEngHor.cumMinEngHor(e)
    image_b,cost=rmHorSeam.rmHorSeam(img,M_up,Tb_up)
    image_list[j][0] = np.copy(image_b)
    Tr[j][0] = Tr[j-1][0]+cost
    T[j][0] = 1

  for i in list(range(1,r)):
    for j in list(range(1,c)):
      img = np.copy(image_list[i][j - 1])
      e_left = genEngMap.genEngMap(img)
      M_left,Tb_left = cumMinEngVer.cumMinEngVer(e_left)
      image_left,cost_left = rmVerSeam.rmVerSeam(img,M_left,Tb_left)

      img = np.copy(image_list[i-1][j])
      e_up = genEngMap.genEngMap(img)
      M_up, Tb_up = cumMinEngHor.cumMinEngHor(e_up)
      image_up, cost_up = rmHorSeam.rmHorSeam(img, M_up, Tb_up)

      cmp_list = [Tr[i,j-1]+cost_left,Tr[i-1,j]+cost_up]
      min_val = min(cmp_list)
      Tr[i,j] = min_val
      min_index = cmp_list.index(min_val)
      T[i,j] = min_index
      if (min_index==0):
        image_list[i][j] = np.copy(image_left)

      else:
        image_list[i][j] = np.copy(image_up)
  Ic = image_list[r-1][c-1]

  #Saving the last frame
  im = Image.fromarray(Ic)
  im.save('Scenary_final.jpg')

  #creating the GIF
  gif_list = [[] for j in range(nr+nc+1)]
  i = nr+nc
  carved_list = backtrack(T,nr,nc,image_list,gif_list,i)

  imageio.mimsave('Scenary.gif', carved_list,duration = 0.2)


  return Ic, Tr

if __name__ == '__main__':
  start_time = time.time()
  r = 33                                                    #Enter the numbers of rows to be removed
  c = 54                                                    #Enter the numbers of coloumns to be removed
  I = np.array(Image.open('Scenary.jpg').convert('RGB'))    #Enter the filename of the image
  Ic,T = carv(I,r,c)
  print("--- %s seconds ---" % (time.time() - start_time))
