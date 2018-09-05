import string
import pylab as pl
import glob
 
from matplotlib import rc
 
USETEX = True
if USETEX:
    rc('font',**{'family':'sans-serif',
                 'sans-serif':['Computer Modern Roman'],
                 'serif':'Computer Modern Roman',
                 'monospace':'Computer Modern Typewriter'})
    rc('text', usetex=True)
 

def line2floats(line):
    try:
        parts = string.split( line )
        floats = map( float, parts)
    except:
        parts = line[0:10], line[10:]
        floats = map( float, parts)
 
    return floats
 

def readTwoColumnFile(fname):
    fid = file(fname,'rt')
    lines = fid.readlines()
    lines = lines[1:] # remove header
 
    data = map(line2floats, lines)
    data = pl.array(data)
    fid.close()
 
    return data

print readTwoColumnFile('selig1210.dat')

