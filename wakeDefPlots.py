#!/usr/bin/env python
# encoding: utf-8
"""
wakeDefPlots.py

Created by Jared J. Thomas on 2015-12-01
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.io import loadmat
from openmdao.api import Problem
from floris_openmdao1 import AEPGroupFLORIS

nTurbines = 2
nDirections = 1
myFloris = Problem(root=AEPGroupFLORIS(nTurbines=nTurbines, nDirections=nDirections, resolution=0.0))
myFloris.setup()

rotorDiameter = 126.4
rotorArea = np.pi*rotorDiameter*rotorDiameter/4.0
axialInduction = 1.0/3.0
CP = 0.7737/0.944 * 4.0 * 1.0/3.0 * np.power((1 - 1.0/3.0), 2)
CT = 4.0*axialInduction*(1.0-axialInduction)
generator_efficiency = 0.944

# set floris parameters
myFloris['floris_params:CPcorrected'] = False
myFloris['floris_params:CTcorrected'] = False
myFloris['floris_params:FLORISoriginal'] = True

# Define turbine characteristics
myFloris['axialInduction'] = np.array([axialInduction, axialInduction])
myFloris['rotorDiameter'] = np.array([rotorDiameter, rotorDiameter])
myFloris['generator_efficiency'] = np.array([generator_efficiency, generator_efficiency])

# Define site measurements
myFloris['windDirections'] = np.array([270.])
myFloris['wind_speed'] = 8.    # m/s
myFloris['air_density'] = 1.1716

myFloris['Ct_in'] = np.array([CT, CT])
myFloris['Cp_in'] = np.array([CP, CP])

FLORISdiams = list()
res = 10000
x = np.linspace(-2*rotorDiameter, 20.0*rotorDiameter, res)
for i in range(0, res):
    X = np.array([0, x[i]])
    Y = np.array([0, 0])
    print myFloris['wakeDiametersT']
    # Y = np.array([0, 0])
    myFloris['turbineX'] = X
    myFloris['turbineY'] = Y

    # Call FLORIS
    myFloris.run()

    FLORISdiams.append(list(myFloris.root.dir0.unknowns['wakeDiametersT']))

FLORISdiams = np.array(FLORISdiams)
FLORISdiams_mat = np.zeros([res, nTurbines, nTurbines, 3])
print FLORISdiams.shape
for i in range(0, nTurbines):
    FLORISdiams_mat[:, i, :, 0] = FLORISdiams[:, 3*nTurbines*i:3*i*nTurbines+nTurbines]
    FLORISdiams_mat[:, i, :, 1] = FLORISdiams[:, 3*nTurbines*i + nTurbines:3*i*nTurbines+2*nTurbines]
    FLORISdiams_mat[:, i, :, 2] = FLORISdiams[:, 3*nTurbines*i + 2*nTurbines:3*i*nTurbines+3*nTurbines]
FLORISindiam = np.array(FLORISdiams_mat[:, 1, 0, 0])
print FLORISindiam.shape
plt.figure()
plt.plot(x/rotorDiameter, FLORISindiam)
plt.show()