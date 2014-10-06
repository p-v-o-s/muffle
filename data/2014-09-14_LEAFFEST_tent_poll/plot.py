from pylab import *
################################################################################
#data processing parameters
IGNORE_FIRST_SAMPLES = 64    #system taking data but not quite stable
CO2_PPM_THRESH_LOW  = 200    #data out of this range is assumed to be corrupt
CO2_PPM_THRESH_HIGH = 5000


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

#-------------------------------------------------------------------------------
#create plot for whole data range
#plotting parameters
FIGSIZE = (16,8)   #inches
XLIM    = (0,60)   #minutes, range of plot

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
ax2.plot(t_min, HUMID_RH, 'c.-', label = "SHT21 Probe", zorder=1)
ax2.set_ylabel(r"Humidity [%RH]")
ax2.legend()
ax2.set_xticklabels([])  #don't show numbers on x axis
ax2.set_xlim(XLIM)

#CO2 level
ax3 = fig.add_subplot(313)
ax3.plot(t_min, CO2_PPM, 'k.-', zorder=1)
ax3.set_ylabel("CO$_2$ Conc. [ppm]")
ax3.set_xlabel("Time [min]")
ax3.set_xlim(XLIM)

#finalize formatting and save plot
fig.tight_layout()             #compresses margins
fig.savefig("Temp-RH-CO2_time_series.svg")        #vector graphics format
fig.savefig("Temp-RH-CO2_time_series.png")        #raster graphics format

#-------------------------------------------------------------------------------
#create annotated plots for initial period
XLIM   = (0,12)
EVENTS = [(3.613,"a",'k'), (4.26,"b",'k'), (5.97,"c",'k'),(7.157,"b",'k'),(8.35,"e",'k'),(9.13,"f",'k')]

ax1.set_xlim(XLIM)
ax2.set_xlim(XLIM)
ax3.set_xlim(XLIM)

y0,y1 = ax1.get_ylim()
ax1_y_avg  = (y1 + y0)/2.0
ax1_y_dif  = (y1 - y0)/2.0

for t_event, label, lc in EVENTS:
    ax1.axvline(x=t_event,ymin=-0.1,ymax=1.0,color=lc,linewidth=2,linestyle="--",zorder=0,clip_on=False)
    ax2.axvline(x=t_event,ymin=-0.1,ymax=1.1,color=lc,linewidth=2,linestyle="--",zorder=0,clip_on=False)
    ax3.axvline(x=t_event,ymin= 0.0,ymax=1.1,color=lc,linewidth=2,linestyle="--",zorder=0,clip_on=False)
    ax1.text(x=t_event,y=ax1_y_avg + 1.025*ax1_y_dif,s=label, horizontalalignment='center')
draw()

#finalize formatting and save plot
fig.tight_layout()             #compresses margins
fig.savefig("Temp-RH-CO2_time_series_annotated.svg")        #vector graphics format
fig.savefig("Temp-RH-CO2_time_series_annotated.png")        #raster graphics format

