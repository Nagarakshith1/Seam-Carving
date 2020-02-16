'''
  File name: rmHorSeam.py
  Author:
  Date created:
'''

'''
  File clarification:
    Removes horizontal seams. You should identify the pixel from My from which 
    you should begin backtracking in order to identify pixels for removal, and 
    remove those pixels from the input image. 
    
    - INPUT I: n × m × 3 matrix representing the input image.
    - INPUT My: n × m matrix representing the cumulative minimum energy map along horizontal direction.
    - INPUT Tby: n × m matrix representing the backtrack table along horizontal direction.
    - OUTPUT Iy: (n − 1) × m × 3 matrix representing the image with the row removed.
    - OUTPUT E: the cost of seam removal.
'''
import numpy as np

def rmHorSeam(I, My, Tby):
  # Your Code Here
  I=np.transpose(I,[1,0,2])
  Mx = My.transpose()
  Tbx = Tby.transpose()
  nr = Mx.shape[0]
  nc = Mx.shape[1]
  E = np.min(Mx[nr - 1])
  Ix = np.zeros((nr, nc - 1, 3), dtype=np.uint8)
  min_x = np.argmin(Mx[nr - 1])
  for i in list(range(nr - 1, 0, -1)):
    Ix[i] = np.delete(I[i], min_x, axis=0)
    if (Tbx[i, min_x] == 1):
      min_x = min_x + 1
    elif (Tbx[i, min_x] == -1):
      min_x = min_x - 1
  Ix[0] = np.delete(I[0], min_x, axis=0)
  Iy = np.transpose(Ix,[1,0,2])
  return Iy, E
