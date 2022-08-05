#!/usr/bin/env python
# this runs on Windows10, queries Keysight counter, and stores data
#-*- coding:utf-8 –*-
#-----------------------------------------------------------------------------
# The short script is a example that open a socket, sends a query,
# print the return message and closes the socket.
#
#No warranties expressed or implied
#
#SIGLENT/JAC 05.2018
#
#-----------------------------------------------------------------------------
import socket # for sockets
import sys # for exit
import time # for sleep
import pyvisa as visa
import os
import math
import numpy as np
from datetime import datetime
from astropy.time import Time
#-----------------------------------------------------------------------------

remote_ip = "10.0.100.112" # should match the instrument’s IP address
#remote_ip = "169.254.2.30"
port = 5025 # the port number of the instrument service

#Port 5024 is valid for the following:
#SIGLENT SDS1202X-E, SDG2X Series, SDG6X Series
#SDM3055, SDM3045X, and SDM3065X 
#
#Port 5025 is valid for the following:
#SIGLENT SVA1000X series, SSA3000X Series, and SPD3303X/XE

count = 0

def SocketConnect():
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('Failed to create socket.')
        sys.exit();
    try:
        #Connect to remote server
        s.connect((remote_ip , port))
    except socket.error:
        print ('failed to connect to ip ' + remote_ip)
    return s

def SocketQuery(Sock, cmd):
    try :
        #Send cmd string
        Sock.sendall(cmd)
        Sock.sendall(b'\n')
        time.sleep(1)
    except socket.error:
        #Send failed
        print ('Send failed')
        sys.exit()
    reply = Sock.recv(4096)
    return reply

def SocketClose(Sock):
    #close the socket
    Sock.close()
    time.sleep(1)

def SocketSend(Sock, cmd):
    try :
        #Send cmd string
        Sock.sendall(cmd)
        Sock.sendall(b'\n')
        time.sleep(1)
    except socket.error:
        #socketSend failed
        print ('Send failed')
        sys.exit()
    return

def SetupKeysight(sigtype):
    s = SocketConnect()
    SocketSend(s,b'*CLS')  #
    #input('should be cleared.  type anything to continue')
    qStr = SocketQuery(s,b'*IDN?')
    print ("IDN= " + str(qStr))
    qStr = SocketQuery(s,b'SYST:ERR?')  #
    print("in first pps area. sigtype="+sigtype)
    if (sigtype=='pps' or sigtype=='mropps'):
      print("in first pps spot. sigtype="+sigtype)
      SocketSend(s,b'CONF:FREQ 1.0,.001')  # this override other commands, so set here
    #if (sigtype=='10MHz' or sigtype=='10mhz' or sigtype=='10mHz' or sigtype=='10Mhz' ):
    if (sigtype=='10mHz'):
      print("in first non-pps spot. sigtype="+sigtype)
      SocketSend(s,b'CONF:FREQ 1.e7,.001')  #this overrides other commands, so set here
      sigtype='10mHz'
    if (sigtype=='t2p' ):
      print("in first non-pps spot. sigtype="+sigtype)
      SocketSend(s,b'CONF:FREQ 1.0,.001')  #this overrides other commands, so set here
      print("did first socketsend")
      SocketSend(s,b'CONF:FREQ 1.0,.001,(@1)')  #this overrides other commands, so set here
      SocketSend(s,b'CONF:FREQ 1.e7,.001,(@2)')  #this overrides other commands, so set here
    SocketSend(s,b'CONF:TINT (@1),(@2)') 
    SocketSend(s,b'INP1:IMP 50') #change 50 to 1.0e6 if want first input to be an f9t device as well
    #input('imp1 should be 50 OHms or 1.0E6  type anything to continue')
    if sigtype=='mropps':
      SocketSend(s,b'INP2:IMP 1.0e6') 
      print('tried to set input 2 to 1 MOhm impedance')
    else:
      SocketSend(s,b'INP2:IMP 50') 
      print('tried to set input 2 to 50 Ohm impedance')
    #input('impedances should be 50 OHms or 1.0E6.  type anything to continue')
    SocketSend(s,b'INP1:LEV:AUTO OFF')  #  
    SocketSend(s,b'INP2:LEV:AUTO OFF')  #  
    #input('INP levels should not be auto.  type anything to continue')
    if (sigtype=='pps' or sigtype=='mropps'):
      print("in second pps spot. sigtype="+sigtype)
      SocketSend(s,b'TRIG:COUN 1')  #  will not return to idle state until N trigger events passed
      SocketSend(s,b'INP1:LEV 1.9')  # 
      SocketSend(s,b'INP2:LEV 1.9')  # 
      SocketSend(s,b'INP1:COUP DC')  #  DC coupling
      SocketSend(s,b'INP2:COUP DC')  #  DC coupling
    if (sigtype=='10mHz'):
      print("in second non-pps spot. sigtype="+sigtype)
      SocketSend(s,b'TRIG:COUN 1')  #  will not return to idle state until N trigger events passed
      # input('trig set  type anything to continue')
      SocketSend(s,b'INP1:LEV 0')  #  
      #input('inp1 level set  type anything to continue')
      SocketSend(s,b'INP2:LEV 0')  # 
      SocketSend(s,b'INP1:COUP AC')  #  AC coupling
      SocketSend(s,b'INP2:COUP AC')  #  AC coupling
    if (sigtype=='t2p'):
      print("in second non-pps spot. sigtype="+sigtype)
      SocketSend(s,b'TRIG:COUN 1')  #  will not return to idle state until N trigger events passed
      # input('trig set  type anything to continue')
      SocketSend(s,b'INP1:LEV 1.9')  #  
      #input('inp1 level set  type anything to continue')
      SocketSend(s,b'INP2:LEV 0')  # 
      SocketSend(s,b'INP1:COUP DC')  #  DC coupling for t2p
      SocketSend(s,b'INP2:COUP AC')  #  AC coupling
    print("to set trigger and sample count")
    SocketSend(s,b'SAMP:COUN 1')  # returns one sample
    SocketSend(s,b'TRIG:SLOP POS')  # positive slope
    SocketSend(s,b'TRIG:DEL 0')  # delay between triggersingle and enabling first  measurement; meas? sets it to 0
    SocketSend(s,b'SYST:TIM 1010')  #  system timeout hopefully 1.01 seconds  needed for Masterclock HQ 53230A
    print("settup done.  readings should follow")
    #input('Keysight setup done.  type anything to continue')
    return s

def main():
    global remote_ip
    global port
    global count
    #pps='n'  # if y does pps setup   if n does 10 MHz
    #pps='y'  # if y does pps setup   if n does 10 MHz
    datadir"C:\\insert_data_dir_here"
    args=sys.argv[1:]
    nargs=len(args)
    print('nargs='+str(nargs))
    if nargs>=1:
      sigtype=sys.argv[1]   
    else:
      sigtype =input('type pps, mropps,10mHz, or t2p')
    badsig='y'
    if (sigtype=='pps' or sigtype=='mropps'):
      badsig='n'
    if (sigtype=='10MHz' or sigtype=='10mhz' or sigtype=='10mHz' or sigtype=='10Mhz'):
      sigtype='10mHz'
      badsig='n'
    if sigtype=='t2p':
      badsig='n' 
    if badsig=='y':
      print("bad input sigtype: "+sigtype+" not supported.  Try pps, 10mHz, or t2p")
      sys.exit()
    #if sigtype !='pps': sigtype='10mHz'
    print("key.py running with sigtype="+sigtype+' now to setup the Keysight counter')
    s=SetupKeysight(sigtype)
    print("now that counter is set up, will change directories to "+datadir)
    #os.chdir("c:\\Users\\Demetrios\\Documents\\python\\keysight")
    os.chdir(datadir)
    errorfile=open("errors.txt","a");
    flag='start'
    nread=0
    while (nread<1000000):
      try:
        nread=nread + 1
        keepgoing=0
        flag='to attempt a read'
        qStr = SocketQuery(s,b'read?') #this did not  work: qStr = SocketQuery(s,b'fetch?') 
        flag='just made a read'
        now=datetime.now()
        seconds_since_epoch=time.time()  #from www.w3resource.com/pythoin/python-date-and-time,=.php
        #utc_date=datetime.utcfromtimestamp(seconds_since_epoch)
        # print("utc_date="+str(utc_date))
        timenow=datetime.utcfromtimestamp(seconds_since_epoch)
        # timenow=now.strftime("%Y-%m-%d %H:%M:%S")
        # print("timenow="+str(timenow))
        flag='just got date'
        xstr=str(qStr)[2:24]
        ns=1.e9*float(xstr)
        times=str(timenow)
        flag='just got times'
        ctimes=times[:10]+'_'+times[11:]
        times=times[:10]+'T'+times[11:]
        t=Time(times)
        flag='just set t'
        mjd=t.mjd
        flag=' mjd ='+str(mjd)+' now to append'
        os.system("echo "+ str(mjd) + " " + str(ns)+ " "+ctimes+" >>"+ str(mjd)[0:5]+ "."+sigtype)  #here it writes outfile file
        flag='appended data'
        print(str(timenow)+" "+str(mjd)+" reads="+str(nread)+', ns=',str(ns),' sigtype=',sigtype)
      except:
        print("problem with talking to keysight at nread="+str(nread)+" flag="+flag)
        errorfile.write(str(timenow)+' nread='+str(nread) + " flag="+flag+'\n')
        os.system("echo "+str(timenow)+" nread="+str(nread) + " flag="+flag+" "+sigtype+" >>"+ "errors.all")
        keepgoing=1
      finally:
        while keepgoing==1:
          try:
            flag='at start of keepgoing loop'
            SocketClose(s)
            flag='closed socket'
            s=SetupKeysight(sigtype)
            #  s = SocketConnect()
            #  qStr = SocketQuery(s,b'SYST:ERR?') 
            #  print ("error was " + str(qStr))
            #  SocketSend(s,b'*CLS') 
            #  flag='syserr='+str(qStr)
            flag='redid setup keepgoing loop'
            keepgoing=0
          except:
             dummy=0
    SocketClose(s)
    print('Query complete. Exiting program')
    sys.exit
# aut does autoscale, probably don't ever want it
# conf:freq 10.0e6,.001   #.001 times freq (10MHz) is resolution  
# conf:tint (@1),(@2)
# SAMP:coun 1   #sample is 1
# TRIG:coun 100  #returns 100 sets
# TRIG:del 1    # sets delay time in seconds between trigger and gate
# read?
#data=socket.recv(1500)
#  qStr = SocketSend(s,b'HCOPY:SDUMP:DATA:FORM   png')  
#  qStr = SocketSend(s,b'HCOPY:SDUMP:DATA?')  #the  screen shows this,
#  qStr = SocketSend(s,b'DISP:text "got this far\n"')  #the  screen shows this,
#  qStr = SocketSend(s,b'DISP:text:cle')  #the  screen clears
#  qStr = SocketSend(s, b'ESR?')  

if __name__ == '__main__':
    proc = main()

