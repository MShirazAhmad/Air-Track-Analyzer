'''
    File name: func.py
    Authors: Muhammad Shiraz Ahmad and Sabieh Anwar
    Date created: 6/22/2019
    Date last modified: 2/22/2020
    Python Version: 3.7.3
'''


'This file contains all the independent useful functions'

import numpy as np


def import_from_physlogger(filename):
    data = np.loadtxt(filename)
    if len(data[0][:])==4:
        data = np.single(data[:, 1:4])
    else:
        data = np.single(data)
    return data


def clipping(data):
    temp = data
    cond_zero = (temp <= 0.7) & (temp <= 1.5)
    cond_one = (temp >= 0.7) & (temp >= 1.5)
    temp[cond_zero] = 0
    temp[cond_one] = 1
    return temp


def indices(CH, time):
    k = 0
    i = 0
    T = []
    while i < (len(CH) - 2):
        if CH[i] == 0 and CH[i + 1] == 1 and CH[i + 2] == 1:
            T.append(time[i + 1])
            k = k + 1
        if CH[i] == 1 and CH[i + 1] == 0 and CH[i + 2] == 0:
            T.append(time[i])
            k = k + 1
        i = i + 1
    return T


def name_list(patharr):
    name=[]
    i=0
    import os
    while i < (len(patharr)):
        name.append(os.path.basename(patharr[i]))
        i=i+1
    return name




def Uaddition(Ux,Uy):
    import numpy as np
    return np.sqrt(Ux**2 + Uy**2)

def Ufraction(X,Ux,Y,Uy):
    import numpy as np
    return np.sqrt((Ux/Y)**2 + ((X*Uy)/(Y**2))**2)
