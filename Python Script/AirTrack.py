'''
    File name: AirTrack.py
    Authors: Muhammad Shiraz Ahmad and Sabieh Anwar
    Date created: 6/22/2019
    Date last modified: 6/22/2019
    Python Version: 3.7.3
'''
def acc(filename):
    import func
    import numpy as np
    acceleration = []
    U_acceleration = []
    for X in filename:
        data = func.import_from_physlogger(str(X))
        channels = func.clipping(data[:, 1:5])

        #Finding the time stamps that correspond to the edges of signal value
        time = data[:, 0]
        T1 = func.indices(channels[:, 0], time)
        T1 = np.single(T1[0:4])
        T2 = func.indices(channels[:, 1], time)
        T2 = np.single(T2[0:4])
        TimeStamp = np.concatenate((T1, T2), axis=None)

        # Finding average acceleration
        Ux = 0.1
        Ux = np.single(Ux)
        Ut = 0.001
        Ut = np.single(Ut)

        flag = 15.25
        flag = np.single(flag)
        V1 = (flag / (TimeStamp[2] - TimeStamp[0]))
        V2 = (flag / (TimeStamp[3] - TimeStamp[1]))
        V3 = (flag / (TimeStamp[6] - TimeStamp[4]))
        V4 = (flag / (TimeStamp[7] - TimeStamp[5]))
        U_V1 = func.Ufraction(flag, Ux, (TimeStamp[2] - TimeStamp[0]), func.Uaddition(Ut, Ut))
        U_V2 = func.Ufraction(flag, Ux, (TimeStamp[3] - TimeStamp[1]), func.Uaddition(Ut, Ut))
        U_V3 = func.Ufraction(flag, Ux, (TimeStamp[6] - TimeStamp[4]), func.Uaddition(Ut, Ut))
        U_V4 = func.Ufraction(flag, Ux, (TimeStamp[7] - TimeStamp[5]), func.Uaddition(Ut, Ut))

        V_AVG = [(V1 + V2) / 2, (V3 + V4) / 2]
        U_V_AVG = [func.Uaddition(U_V1, U_V2), func.Uaddition(U_V3, U_V4)]
        U_V_AVG = np.single(U_V_AVG)
        T_AVG = [0.5 * ((0.5 * (TimeStamp[0] + TimeStamp[1])) + (0.5 * (TimeStamp[2] + TimeStamp[3]))),
                 0.5 * ((0.5 * (TimeStamp[4] + TimeStamp[5])) + (0.5 * (TimeStamp[6] + TimeStamp[7])))]
        U_T_AVG = [func.Uaddition(func.Uaddition(Ut, Ut), func.Uaddition(Ut, Ut)), func.Uaddition(func.Uaddition(Ut, Ut), func.Uaddition(Ut, Ut))];

        ACC = (V_AVG[1] - V_AVG[0]) / (T_AVG[1] - T_AVG[0])

        X_ACC = (V_AVG[1] - V_AVG[0])
        U_X_ACC = func.Uaddition(U_V_AVG[1], U_V_AVG[0])

        Y_ACC = (T_AVG[1] - T_AVG[0])
        U_Y_ACC = func.Uaddition(U_T_AVG[1], U_T_AVG[0])

        U_ACC = func.Ufraction(X_ACC, U_X_ACC, Y_ACC, U_Y_ACC)
        acceleration.append(ACC)
        U_acceleration.append(U_ACC)
    return acceleration, U_acceleration
