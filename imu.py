import spidev
import time
import argparse
import sys
import navio.mpu9250
import navio.util
import numpy as np

navio.util.check_apm()

imu = navio.mpu9250.MPU9250()

if imu.testConnection():
    print "Connection established: True"
else:
    sys.exit("Connection established: False")

imu.initialize()

time.sleep(1)

outdata=np.zeros((600,10))
cnt=0
while True:
	# imu.read_all()
	# imu.read_gyro()
	# imu.read_acc()
	# imu.read_temp()
	# imu.read_mag()

	# print "Accelerometer: ", imu.accelerometer_data
	# print "Gyroscope:     ", imu.gyroscope_data
	# print "Temperature:   ", imu.temperature
	# print "Magnetometer:  ", imu.magnetometer_data

	# time.sleep(0.1)

	m9a, m9g, m9m = imu.getMotion9()

	print "Acc:", "{:+7.3f}".format(m9a[0]), "{:+7.3f}".format(m9a[1]), "{:+7.3f}".format(m9a[2]),
	print " Gyr:", "{:+8.3f}".format(m9g[0]), "{:+8.3f}".format(m9g[1]), "{:+8.3f}".format(m9g[2]),
	print " Mag:", "{:+7.3f}".format(m9m[0]), "{:+7.3f}".format(m9m[1]), "{:+7.3f}".format(m9m[2])
	#system time
	outdata[cnt,0]=time.time()
	#Accelerometer
	outdata[cnt,1]=m9a[0]
	outdata[cnt,2]=m9a[1]
	outdata[cnt,3]=m9a[2]
	#Gyroscope
	outdata[cnt,4]=m9g[0]
	outdata[cnt,5]=m9g[1]
	outdata[cnt,6]=m9g[2]
	#Magnetometer
	outdata[cnt,7]=m9m[0]
	outdata[cnt,8]=m9m[1]
	outdata[cnt,9]=m9m[2]
	cnt+=1
	if cnt>=600:
		cnt=0
		np.savetxt('DATA/imu_'+time.strftime('%Y%m%d-%H%M%S')+'.dat',outdata)
		outdata=np.zeros((600,10))

	time.sleep(0.1)
