
import ROOT
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def convertHisto(file, histoname):

# x-axis: time
# y-axis: wires

    histo = file.Get(histoname)
    print "reading " + histoname

    NBinsX = histo.GetNbinsX()
    NBinsY = histo.GetNbinsY()

    array = np.zeros([NBinsX, NBinsY])
    for wires in range(NBinsY):
        for ticks in range(NBinsX):
            bin = histo.GetBin(ticks, wires)
            array[ticks, wires] = histo.GetBinContent(bin)

    return array




prefixInduction = "Ind_"
prefixCollection = "Col_"

f = ROOT.TFile(filename)

filename = './data/Run_00050010.root'
# Convert a TTree in a ROOT file into a NumPy structured array

# x-axis: time
# y-axis: wires
histoname = prefixCollection + str(2)

array = convertHisto(f,prefixCollection+"0")





#plotting
im = plt.imshow(array, interpolation='bilinear', cmap=cm.hsv,
                origin='lower',
                vmax=abs(array).max(), vmin=-abs(array).max()/0.7 ,aspect=0.01)
plt.show()




