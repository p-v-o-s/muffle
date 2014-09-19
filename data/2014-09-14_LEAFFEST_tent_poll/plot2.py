from pylab import *
################################################################################
#data processing parameters
IGNORE_FIRST_SAMPLES = 64    #system taking data but not quite stable
CO2_PPM_THRESH_LOW  = 200    #data out of this range is assumed to be corrupt
CO2_PPM_THRESH_HIGH = 5000


#load and process data
D = loadtxt("LOGGER99.csv",comments="#", delimiter=",", usecols=(0,2,3,4,5))
D2 = D[IGNORE_FIRST_SAMPLES:]  #remove first bunch of rows
DATETIME,RTC_TEMP_C,TEMP_C,HUMID_RH,CO2_PPM = D2.transpose() #split into columns
t_sec = DATETIME - DATETIME[0]
t_min  = t_sec/60.0

for i in range(1,CO2_PPM.shape[0]):  #filter out bad sensor values of CO2
    v = CO2_PPM[i]
    if v < CO2_PPM_THRESH_LOW or v > CO2_PPM_THRESH_HIGH:
        CO2_PPM[i] = CO2_PPM[i-1]    #replace with last value

#plot first segment of data
x1 = 1000         #around 25 min
x2 = x1 + 1300    #around 60 min

H2 = HUMID_RH[x1:x2]
C2 = CO2_PPM[x1:x2]
t2 = t_min[x1:x2]

#rescale the data units
nC = (C2 - C2.mean())/C2.std()
nH = (H2 - H2.mean())/H2.std()


fig = figure()
ax = fig.add_subplot(111)
ax.plot(t2,nH, 'c.-', label = 'norm. RH')
ax.plot(t2,nC,'k.-', label = 'norm. CO2')
ax.set_title("Humidity and CO$_2$ Fluctuations During Sleep, Segment 1")
legend()
fig.savefig("RH-CO2_fluctuations_during_sleep_seg1.png")

#plot the second segment of data
H2 = HUMID_RH[x2:]
C2 = CO2_PPM[x2:]
t2 = t_min[x2:]

#rescale the data units
nC = (C2 - C2.mean())/C2.std()
nH = (H2 - H2.mean())/H2.std()


fig = figure()
ax = fig.add_subplot(111)
ax.plot(t2,nH, 'c.-', label = 'norm. RH')
ax.plot(t2,nC,'k.-', label = 'norm. CO2')
ax.set_title("Humidity and CO$_2$ Fluctuations During Sleep, Segment 2")
legend()
fig.savefig("RH-CO2_fluctuations_during_sleep_seg2.png")
