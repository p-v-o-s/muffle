from pylab import *
from scipy.signal import medfilt
D = loadtxt("LOGGER99.csv",comments="#", delimiter=",", usecols=(0,2,3,4,5)).transpose()
DATETIME,RTC_TEMP_C,TEMP_C,HUMID_RH,CO2_PPM = D
t_secs = DATETIME - DATETIME[0]
t_min  = t_secs/60.0
fig = figure()

#temperatures
ax1 = fig.add_subplot(311)
ax1.plot(t_min, RTC_TEMP_C, 'r.-', label="RTC")
ax1.plot(t_min, TEMP_C, 'b.-', label = "SHT21 Probe")
ax1.set_ylabel("Temperature [$^\circ$C]")
ax1.legend()

#humidity
ax2 = fig.add_subplot(312)
ax2.plot(t_min, HUMID_RH, 'c.-')
ax2.set_ylabel("Humidity [%%RH]")

#CO2 level
CO2_PPM = medfilt(CO2_PPM,3)  #clean up noise spikes of size 1
CO2_PPM = medfilt(CO2_PPM,5)  #clean up noise spikes of size 2-3
ax3 = fig.add_subplot(313)
ax3.plot(t_min, CO2_PPM, 'k.-')
ax3.set_ylabel("CO$_2$ Concentration [ppm]")


show()
