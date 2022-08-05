print('this is appendfile.  input string is infile, outfile, MJDmin, MJDmax');
import math
#import matplotlib
#import matplotlib.pyplot as plt
import os
import time
import sys
verbose='n'
#print('importing done now to read infile');
args=sys.argv[1:]
nargs=len(args)
#print ('sysarv0='+sys.argv[0])
print ('nargs=',str(nargs))
infile=sys.argv[1]   #sys.arv[0] is the appendfile.py
print('infile='+infile)
outfile=sys.argv[2]
print('outfile='+outfile)
mjdmin=float(sys.argv[3])
mjdmax=float(sys.argv[4])
print('mjdmin='+str(mjdmin)+' mjdmax=',str(mjdmax))
filein=open(infile,"r");
fileout=open(outfile,"a");
iend=0
nread=0
nwrite=0
while nread>-1:
  if verbose=='y': print('to read a line')
  data=filein.readline()
  if data=='':
    print('end of file reached by appendfiles.py nread=',nread,' nwrite=',nwrite,' thats all folks')
    exit() 
  nread=nread+1
  line=str.split(data,' ') # the demarker is a blank
  if verbose=='y': print('line0='+line[0])
  try:
    first=float(line[0])
    if first>=mjdmin and first<=mjdmax:
      if verbose=='y':
         print('first passed inclusion test. first='+str(first))
         print('data=',data)
         print('outfile=',outfile)
         # exit()
      fileout.write(data)
      nwrite=nwrite+1
    if verbose=='y': print('first='+str(first)+' nwrite='+str(nwrite))
  except:
    print('fatal problem at nread=',nread,' data=',data)
    print('first=',first)
    exit()
