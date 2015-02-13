from rootpy.interactive import wait
import ROOT
from rootpy.plotting import Hist, Hist2D, Hist3D, HistStack, Legend, Canvas, utils
from rootpy.io import File

from matplotlib import pyplot as plt
from rootpy.io import root_open
import numpy as np
filename = './data/Run_00050001.root'
# Convert a TTree in a ROOT file into a NumPy structured array


f = root_open(filename, 'read')

# get the list of histograms in the file
hsitos = list(f)



# get the iterators for the histograms
xbins = hsitos[2].bins_range(axis=0)
ybins = hsitos[2].bins_range(axis=1)
rangeX = len(xbins)
rangeY = len(ybins)
array = np.zeros([rangeX, rangeY])


for i in range(rangeX):
    for j in range(rangeY):
        array[i, j] = hsitos[2][i, j].value


