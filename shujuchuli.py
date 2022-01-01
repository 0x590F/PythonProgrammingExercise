import os
import h5py
from numpy import *
import numpy as np

count = 0
str_file=os.getcwd()
stindex = 0
for dirpaths, dirnames, filenames in os.walk(str_file):
    for filename in filenames:
        if ".h5" in filename:
            #file_name = str_file + filename
            #print(file_name)
            hdffile = h5py.File(filename, 'r')
            filename=filename.split(".h5")[0]
            print (filename)
            freqLOnum = filename.split("GHz")[0].split("_")[1]
            freqLOnum = float(freqLOnum)*(10**9)

            span = filename.split("MHz")[0].split("_")[2]
            span = float(span)*(10**6)

            sweetPoint = filename.split("_LO")[0].split("_")[3]
            sweetPoint  = float(sweetPoint)

            print(freqLOnum,span,sweetPoint)
            print ('\n')

            pts = int(sweetPoint)
            
            mags = hdffile['iqdata_raw']['keyint_192']['keystr_stream_mag'][stindex : (stindex+2*pts):2]
            phase = hdffile['iqdata_raw']['keyint_192']['keystr_stream_phase'][stindex : (stindex+2*pts):2]

            start_carrier = freqLOnum - span/2.0
            end_carrier =  freqLOnum + span/2.0
            inc_carrier =  span / sweetPoint
            carrier_freqs = arange(start_carrier ,end_carrier,inc_carrier)

            np.savetxt(filename +'.txt', np.column_stack((carrier_freqs,mags,phase)),header='Freq(Hz)            I              Q',delimiter='\t')
            count = count + 1
print(count)
