print('this is unwrap. infile, outfile (or x), mingap,10mHz or pps or 100, sec (anything else makes units ns), and units - default being ns');
#unwrap.py adjusts input data to remove phase wraps
# output is timetag, phase-wrap corrected adjusted time,nreadl,sidereal time approximation,timetag modulo 0, orignal datum, dy
# nread added to output on 12apr2021
# mingap is minimum gap size before uses extrapolation to find jumps
import math
#import matplotlib
#import matplotlib.pyplot as plt
import os
import time
import sys
print('unwrap done importing.  now to read infile');
dir=os.path.dirname(os.path.realpath(__file__));
print('dir=',dir);
args=sys.argv[1:]
nargs=len(args)
print ('sysarv0='+sys.argv[0])
print ('nargs=',str(nargs))
infile=sys.argv[1]   #sys.arv[0] is the unwrap.py
print('infile='+infile)
mingap=0
if nargs>1:
  outfile=sys.argv[2]
  lout=int(len(outfile))
  if (lout==1):
      outfile=infile+'.unwrap'
print('outfile='+outfile)
if infile==outfile:
  print('unwrap quitting because infile == outfile!')
  exit()
if nargs>2: 
  cmingap=str(sys.argv[3])
  print('cmingap='+cmingap)
  mingap=float(cmingap)
quant=1000000000  # default units are nanoseconds, this is therefore one second
if nargs>3:
  cquant=str(sys.argv[4])
  print('cquant='+cquant)
  if (cquant=='10' or cquant=='100' or cquant=='10mHz' or cquant=='10mhz' or cquant=='10Mhz' or cquant=='10MHz'): 
    cquant='100'
    quant=100
  if (cquant=='pps' or cquant=='PPS'): 
    cquant='1000000000'
    quant=1000000000
if nargs>4: 
  cunit=str(sys.argv[5])
  print('cunit='+cunit)
  if cunit=='sec' or cunit=='seconds':
     quant=quant/1.e9
print('quant='+str(quant))
quant2=quant/2
filein=open(infile,"r");
fileout=open(outfile,"w");
iend=0
name='skip'
nread=0
yold=0
yolder=0
nwrite=0
mjdold=0
mjd=0
while nread>-1:
 if iend==1:
   print('unwrap done.  nread='+str(nread)+' nwrite='+str(nwrite)+' infile='+infile+' out='+outfile+' thats all folks.')
   exit()
 if iend==0:
  data=filein.readline()
  nread=nread+1
  if data=='':
    print('end of file reached nread=',nread)
    iend=1
    break
    #time.sleep(5)
    #os.system("pause")
  #print('data='+data)
  line=str.split(data,' ') # the demarker is a blank.  will fail if demarker is a coma
  #  print('line0='+line[0])
  try:
    first=line[0]
    mjdolder=mjdold
    mjdold=mjd
    dxold=mjdold-mjdolder
    mjd=float(first)
    dx=mjd-mjdold
    mjdint=int(mjd)
    mjdsid=(mjd-59140)*366.25/365.25
    sid=mjdsid-int(mjdsid)
    next=line[1]
    #print('next='+next)
    y=float(next)
    l=len(first)
    chars=list(first)
    #print('nread',nread,' data=',data,' first=',first,' y=',str(y))
    #print('that went well')
  except:
    print('problem at nread=',nread,' data=',data)
    print('first=',first)
    print('next=',next)
    break 
  ysave=y
  if (nread>3 and dx-dxold>.1*dxold and dx>mingap):yold=yold+(yold-yolder)*dx/(dxold)
  dy=y-yold
  ncor=0
  ndy=0
  toround=0
  nflag=0
  if dy>quant2:
    # print('dy too large='+str(dy))
    toround=dy/quant
    ndy=round(toround,0)
    ncor=-ndy*quant
    y=y+ncor
    # print('y now='+str(y)+' ndy=',str(ndy)+' tround=',str(toround))
    nflag=1
  if dy<-quant2:
    # print('dy too small='+str(dy))
    toround=-dy/quant
    ndy=round(toround,0)
    ncor=ndy*quant
    y=y+ncor
    nflag=2
  # print(' y='+str(y)+' yold='+str(yold))
  #  lineout=first+' '+str(y)+' ysave='+str(ysave)+' dy='+str(dy)+' ndy='+str(ndy)+' ncor='+str(ncor)+' toround='+str(toround)+' nflag='+str(nflag)+' quant='+str(quant)+' quant2='+str(quant2)+'\n'
  lineout=first+' '+str(y)+' '+str(nread)+' '+str(sid)+' '+str(mjd-mjdint)+' ysave= '+str(ysave)+' dy= '+str(dy)+' ndy= '+str(ndy)+' ncor= '+str(ncor)+' toround= '+str(toround)+' nflag= '+str(nflag)+' quant= '+str(quant)+' quant2= '+str(quant2)+' '+data
  fileout.write(lineout)
  #  if nread==14:exit()  #  REMOVE ME
  nwrite=nwrite+1
  yolder=yold
  yold=y
  #time.sleep(5)
 #except:
   #name='skip'
   #print('some exception found at nread=',nread)
 #else:
   #print('no problemo. nread=',str(nread))
  # except:
  # print('bad read',next)
print('thats all folks, unwrap infile=',infile,' nread=',str(nread),' nwrite=',str(nwrite));
exit()
