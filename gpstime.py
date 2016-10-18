import serial
import pynmea2
import time
import numpy as np

try:
	ser = serial.Serial('/dev/pts/2',4800)
	seria = 1
except:
	seria = 0

try:

	outdata=np.zeros((100,5))
	cnt=0
	intt=round(time.time())

	while seria:
		data = ser.readline()
		#print data
		if (data.startswith("$GNRMC")):
			msg1=pynmea2.parse(data)
			#print msg1.datetime
			#print time.time()
			#print time.mktime(msg1.datetime.timetuple())
	        if (data.startswith("$GNGGA")):
        	        msg2=pynmea2.parse(data)
                	print msg2.latitude
			print msg2.longitude
			print msg2.altitude
			print msg1.datetime

			outdata[cnt,0]=time.time()
			outdata[cnt,1]=time.mktime(msg1.datetime.timetuple())
			outdata[cnt,2]=msg2.latitude
			outdata[cnt,3]=msg2.longitude
			outdata[cnt,4]=msg2.altitude

			cnt+=1

			print round(time.time())-intt
			if (round(time.time())-intt>=60):
				print 'TAK'
				cnt=0
				intt=round(time.time())
				if cnt==0:
					print 'SAVE'
					np.savetxt('DATA/gps_'+time.strftime('%Y%m%d-%H%M%S')+'.dat',outdata)
					print 'SAVEt'
					outdata=np.zeros((100,5))


except:
	print "QAZ"
