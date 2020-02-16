'''
  File name: cumMinEngVer.py
  Author:
  Date created:
'''

'''
  File clarification:
    Computes the cumulative minimum energy over the vertical seam directions.
    
    - INPUT e: n × m matrix representing the energy map.
    - OUTPUT Mx: n × m matrix representing the cumulative minimum energy map along vertical direction.
    - OUTPUT Tbx: n × m matrix representing the backtrack table along vertical direction.
'''
import numpy as np
import copy

def cumMinEngVer(e):
  # Your Code Here
  nr = e.shape[0]
  nc = e.shape[1]
  Tbx = np.zeros((nr,nc))
  e_copy = copy.deepcopy(e)
  up_neighbour = np.append(np.Inf*np.ones((1,nc)),np.delete(e_copy,nr-1,0),axis=0)
  right_up_neighbour = np.append(np.delete(up_neighbour,0,1),np.Inf*np.ones((nr,1)),axis=1)

  left_up_neighbour = np.append(np.Inf*np.ones((nr,1)),np.delete(up_neighbour,nc-1,1),axis=1)
  Mx = copy.deepcopy(e)

  for i in list(range(1,nr)):
    min_first = np.minimum(left_up_neighbour[i], right_up_neighbour[i])
    Mx[i] = Mx[i] + np.minimum(min_first,up_neighbour[i])
    stack = np.vstack((left_up_neighbour[i],up_neighbour[i],right_up_neighbour[i]))
    Tbx[i] = np.argmin(stack,axis=0) - 1
    if(i+1<nr):
      up_neighbour[i+1] = Mx[i]
      right_up_neighbour[i+1,:-1] = Mx[i,1:]
      left_up_neighbour[i+1, 1:] = Mx[i, :-1]
  return Mx, Tbx

