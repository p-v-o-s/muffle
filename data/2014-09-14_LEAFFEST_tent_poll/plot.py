from pylab import *

#data processing parameters
IGNORE_FIRST_SAMPLES = 64    #system taking data but not quite stable
CO2_PPM_THRESH_LOW  = 200    #data out of this range is assumed to be corrupt
CO2_PPM_THRESH_HIGH = 5000

#plotting parameters
FIGSIZE = (16,8)   #inches
XLIM    = (0,60)   #minutes, range of plot

#load and process data
D = loadtxt("LOGGER99.csv",comments="#", delimiter=",", usecols=(0,2,3,4,5))
D = D[IGNORE_FIRST_SAMPLES:,]  #remove first bunch of rows
DATETIME,RTC_TEMP_C,TEMP_C,HUMID_RH,CO2_PPM = D.transpose() #split into columns
t_secs = DATETIME - DATETIME[0]
t_min  = t_secs/60.0

for i in range(1,CO2_PPM.shape[0]):  #filter out bad sensor values of CO2
    v = CO2_PPM[i]
    if v < CO2_PPM_THRESH_LOW or v > CO2_PPM_THRESH_HIGH:
        CO2_PPM[i] = CO2_PPM[i-1]    #replace with last value

#create plot
fig = figure(figsize=FIGSIZE)

#temperatures
ax1 = fig.add_subplot(311)
ax1.plot(t_min, RTC_TEMP_C, 'r.-', label="RTC")
ax1.plot(t_min, TEMP_C, 'b.-', label = "SHT21 Probe")
ax1.set_ylabel("Temperature [$^\circ$C]")
ax1.legend()
ax1.set_xticklabels([])  #don't show numbers on x axis
ax1.set_xlim(XLIM)

#humidity
ax2 = fig.add_subplot(312)
ax2.plot(t_min, HUMID_RH, 'c.-')
ax2.set_ylabel(r"Humidity [%RH]")
ax2.set_xticklabels([])  #don't show numbers on x axis
ax2.set_xlim(XLIM)

#CO2 level
ax3 = fig.add_subplot(313)
ax3.plot(t_min, CO2_PPM, 'k.-')
ax3.set_ylabel("CO$_2$ Conc. [ppm]")
ax3.set_xlabel("Time [min]")
ax3.set_xlim(XLIM)

#finalize formatting and save plot
fig.tight_layout()             #compresses margins
fig.savefig("Temp-RH-CO2_time_series.svg")        #vector graphics format
fig.savefig("Temp-RH-CO2_time_series.png")        #raster graphics format
