# f9t-device-testing

Python scripts for comparing the differences of 2 PPS sources.  

## Overview of Scripts  

key.py (best to perform in powershell)  
Controls the counter and writes the data into the dir you are in.  
Files would have names like '59700.pps', formatted with the current MJD.  
When using f9t devices (or anything requiring an mro), ensure that you use the "mropps" argument rather then the "pps" argument when issuing the command -- example below  
cd/.../data_dir  
python key.py mropps #sets to 1Mohm impedance for f9t-like devices  
#additional arguments include 10mhz or t2p for tick to phase  




unwrap.py (best to perform in windows command line)  
Adjusts the data output of key.py by taking out the 1-second jumps. So if the data goes rom .0001 to .99999, it makes the last point -.00001 seconds.     
usage:  
set mjd=59700  
python unwrap.py %mjd%.mropps %mjd%.unwrapped 1 pps ns  




appendfile.py (best to perform in windows command line)    
Takes out the part of th emjd-named file that you want and appends it to the final file for plotting, etc.    
usage:  
set outfile=example_file_name.txt  
python appendfile.py 59700.unwrapped %outfile% 0 99999  
python appendfile.py 59701.unwrapped %outfile% 0 99999  
python appendfile.py 59702.unwrapped %outfile% 0 99999  
#repeat for each collected date that you want to be combined into the %outfile%  



Additional notes:  
add your actual dir you want file to be stored in to line 156 on the key.py before running for the first time  
make sure that you change the ip address in key.py to what your keysight device ip is
