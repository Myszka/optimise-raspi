import threading
import time
import sys
import Queue
import navio.leds
import navio.util
import seabreeze
import numpy as np
seabreeze.use('pyseabreeze')
import seabreeze.spectrometers as sb

navio.util.check_apm()
led = navio.leds.Led()

#spec0.integration_time_micros(400000)
#spec1.integration_time_micros(1800000)

def optuSpec(spec,mini=0,maxi=2):
	led.setColor('Red')
	intens=0
	inttime=mini*1e6-100000
	if inttime<0:
		inttime=0
	while intens<14500 and inttime<maxi*1e6:
		inttime+=100000
		spec.integration_time_micros(inttime)
		led.setColor('Blue')
		intens=max(spec.intensities())
		led.setColor('Red')
		print "time: "+str(inttime/1e6)+" / intensity: "+str(intens)
	led.setColor('Green')
#	np.savetxt('STS'+spec.serial_number+'-inttime.log',[inttime],delimiter=',')
	return inttime

def getBlack(spec):
	#ress=[]
	spec0=spec
	nrmsmt=20
#	spec0.integration_time_micros(float(np.genfromtxt('STS'+spec0.serial_number+'-inttime.log')))
	out0=np.zeros((nrmsmt+1,1025))
	out0[0,:-1]=spec0.wavelengths()
	for i in np.arange(1,nrmsmt+1):
		out0[i,:-1]=spec0.intensities()
		out0[i,-1]=time.time()
		print '#'+str(i)+' '
	np.savetxt('STS'+spec.serial_number+'-dark.log',out0.T,delimiter=',')

def stswait(czas,kolor=['Red','Black']):
	led.setColor('Black')
	cnt=0
	while cnt<czas:
		led.setColor(kolor[cnt%2])
		time.sleep(1)
		cnt+=1
		print czas-cnt
	led.setColor('Black')


devices = sb.list_devices()
nospec=len(devices)

#Present number of Spectrometers with red blinks
print "Number of devices"+str(nospec)

#stswait(nospec*2+1,['Green','Red'])

#Wait 45 seconds for optimilisation of integration time
#print "Prepare for integration time measurement"
#stswait(15,['Green','Yellow'])

print "Integration time test"
if nospec>1:
	global spec0
	global spec1
	spec0 = sb.Spectrometer(devices[0])
	spec1 = sb.Spectrometer(devices[1])

	#spec0IT=optuSpec(spec0,mini=0,maxi=2)
	#spec3IT=optuSpec(spec1,mini=0,maxi=2)

#Wait 45 minutes for dark msmt
print "Prepare for black measurements"
#stswait(25,['Black','Yellow'])
print "Black measurements"

if nospec>1:

	spec0.integration_time_micros(2e6)
	spec1.integration_time_micros(8e5)

	getBlack(spec0)
	getBlack(spec1)

#Wait before flight
print "Prepare for flight"
#stswait(20,['Green','Blue'])

print "FLIGHT!"

def getSpec0():
	#ress=[]
	while True:
		out0=np.zeros((101,1025))
		out0[0,:-1]=spec0.wavelengths()
		for i in np.arange(1,101):
			out0[i,:-1]=spec0.intensities()
			out0[i,-1]=time.time()
			print '#'+str(i)+' '
		np.savetxt('DATA/sts'+spec0.serial_number+'_'+time.strftime('%Y%m%d-%H%M%S')+'.dat',out0.T,delimiter=',')

	#return ress

def getSpec1():
	#ress=[]
	while True:
		out1=np.zeros((101,1025))
		out1[0,:-1]=spec1.wavelengths()
		for i in np.arange(1,101):
			out1[i,:-1]=spec1.intensities()
			out1[i,-1]=time.time()
			print time.time()
		np.savetxt('DATA/sts'+spec1.serial_number+'_'+time.strftime('%Y%m%d-%H%M%S')+'.dat',out1.T,delimiter=',')

global start_time
start_time=time.time()+5

def read0():
    while time.time() <= start_time:
        pass
    threading.Thread(target=getSpec0).start()
def read1():
    while time.time() <= start_time:
        pass
    threading.Thread(target=getSpec1).start()
threading.Thread(target=read0).start()
threading.Thread(target=read1).start()


#spec0.close()
#spec1.close()
