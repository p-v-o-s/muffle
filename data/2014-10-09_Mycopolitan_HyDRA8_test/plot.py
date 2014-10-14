from pylab import *
import datetime
################################################################################
#data processing parameters
IGNORE_FIRST_SAMPLES = 64    #system taking data but not quite stable
CO2_PPM_THRESH_LOW  = 200    #data out of this range is assumed to be corrupt
CO2_PPM_THRESH_HIGH = 5000


#load and process data
D = loadtxt("LOGGER00.CSV",comments="#", delimiter=",", usecols=(0,2,3,4,5))
D2 = D[IGNORE_FIRST_SAMPLES:]  #remove first bunch of rows
TIMESTAMP,RTC_TEMP_C,TEMP_C,HUMID_RH,CO2_PPM = D2.transpose() #split into columns
t_sec = TIMESTAMP - TIMESTAMP[0]
t_min  = t_sec/60.0
t_hour = t_min/60.0

DT =  array(map(datetime.datetime.fromtimestamp,TIMESTAMP))


for i in range(1,CO2_PPM.shape[0]):  #filter out bad sensor values of CO2
    v = CO2_PPM[i]
    if v < CO2_PPM_THRESH_LOW or v > CO2_PPM_THRESH_HIGH:
        CO2_PPM[i] = CO2_PPM[i-1]    #replace with last value

#-------------------------------------------------------------------------------
#create plot for whole data range
#plotting parameters
FIGSIZE = (16,8)   #inches

fig = figure(figsize=FIGSIZE)

#temperatures
convCtoF = lambda c: 9.0/5.0*c  + 32.0
ax1_C = fig.add_subplot(311) # Celcius axis
#ax1.plot(t_hour, RTC_TEMP_C, 'r.-', label="RTC")
ax1_C.plot(DT, TEMP_C, 'b.-', label = "SHT21 Probe")
ax1_C.set_ylabel("Temperature [$^\circ$C]")
ax1_C.legend()
ax1_C.set_xticklabels([])  #don't show numbers on x axis
ax1_F = ax1_C.twinx()        #Farenheit axis
y_min, y_max = ax1_C.get_ylim()
ax1_F.set_ylim((convCtoF(y_min),convCtoF(y_max)))
ax1_F.set_ylabel("Temperature [$^\circ$F]")




#humidity
ax2 = fig.add_subplot(312)
ax2.plot(DT, HUMID_RH, 'c.-', label = "SHT21 Probe", zorder=1)
ax2.set_ylabel(r"Humidity [%RH]")
ax2.legend()
ax2.set_xticklabels([])  #don't show numbers on x axis

#CO2 level
ax3 = fig.add_subplot(313)
ax3.plot(DT, CO2_PPM, 'k.-', zorder=1)
ax3.set_ylabel("CO$_2$ Conc. [ppm]")
ax3.set_xlabel("Time [EST]")

#finalize formatting and save plot
fig.tight_layout()             #compresses margins
fig.savefig("Temp-RH-CO2_time_series.svg")        #vector graphics format
fig.savefig("Temp-RH-CO2_time_series.png")        #raster graphics format

show()
