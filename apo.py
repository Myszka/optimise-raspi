import sys, time
import numpy as np
import navio.adc
import navio.util

navio.util.check_apm()

adc = navio.adc.ADC()
results = [0] * adc.channel_count

outdata=np.zeros((600,3))
cnt=0

while (True):
    outdata[cnt,0]=time.time()
    outdata[cnt,1]= adc.read(4)*5
    outdata[cnt,2]= adc.read(5)*5
    print "t: "+str(outdata[cnt,0])+" Sa: "+str(outdata[cnt,1])+"umol m^-2 s^-1 Sb: "+str(outdata[cnt,2])+"umol m^-2 s^-1"
    cnt+=1
    if cnt>=600:
    	cnt=0
    	np.savetxt('DATA/apogee_'+time.strftime('%Y%m%d-%H%M%S')+'.dat',outdata)
    	outdata=np.zeros((600,3))
    time.sleep(0.1)
