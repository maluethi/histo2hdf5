import tables as tbl
import sys
import getopt

import ROOT

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt


# @profile
# noinspection PyPep8Naming
def readHisto(filename, histoname):
    # reads an TH2 histogram from file and returns it as an numpy array.
    # x-axis: time
    # y-axis: wires

    histo = filename.Get(histoname)
    print "reading " + histoname

    NBinsX = histo.GetNbinsX()
    NBinsY = histo.GetNbinsY()
    binHisto = 0
    array = np.zeros([NBinsX, NBinsY], dtype=int)
    for wires in range(NBinsY):
        for ticks in range(NBinsX):
            binHisto = histo.GetBin(ticks, wires)
            array[ticks, wires] = histo.GetBinContent(binHisto)
            #binHisto += 1

    return array


def plotEvent(array):
    # simple plotting to verify data
    im = plt.imshow(array, interpolation='bilinear', cmap=cm.hsv,
                    origin='lower',
                    vmax=abs(array).max(), vmin=-abs(array).max() / 0.7, aspect=0.01)
    plt.show()


# noinspection PyPep8Naming
def main(argv):
    prefixInduction = "Ind_"
    prefixCollection = "Col_"

    # logics to detect wrong inputs
    RunNumber = ''
    try:
        opts, args = getopt.getopt(argv, "hr:", ["ifile="])
    except getopt.GetoptError:
        print 'test.py -r <RunNumber>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -r <RunNumber>'
            sys.exit()
        elif opt in "-r":
            RunNumber = str(arg)

    print "Converting Run " + RunNumber

    # file names & definitions
    RunNumber = RunNumber.zfill(8)
    filename = 'Run_' + RunNumber
    RunSize = 200
    DataDirectory = './data/'
    RootFilename = DataDirectory + filename + '.root'
    H5Filename = DataDirectory + filename + '.h5'


    f = ROOT.TFile(RootFilename)

    # construct file structure in hdf5 file,
    h5file = tbl.open_file(H5Filename, mode="w", title=RunNumber)
    info = h5file.create_group(h5file.root, "info", "Run Information")
    data = h5file.create_group(h5file.root, "data", "Stored Data")

    # Convert a TTree in a ROOT file into a NumPy structured array

    # x-axis: time
    # y-axis: wires
    # read and write events to file
    for i in range(RunSize):
        event = h5file.create_group(data, "event" + str(i).zfill(3), "Event " + str(i))
        collection = readHisto(f, prefixCollection + str(i))
        induction = readHisto(f, prefixInduction + str(i))
        h5file.create_array(event, 'collection', collection, "Collection Plane Data")
        h5file.create_array(event, 'induction', induction, "Induction Plane Data")

    h5file.close()


if __name__ == "__main__":
    main(sys.argv[1:])


