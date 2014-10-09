#include <JeeLib.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <RTClib.h>
#include <RTC_DS3231.h>
#include <SHT2x.h>
#include <stdlib.h>
#include <SoftwareSerial.h>


#define led 16 //indicator led


#define debug 0 //whether or not to print statements out on serial

//sleeping
//ISR(WDT_vect) { Sleepy::watchdogEvent(); }
#define LOG_INTERVAL_BASE  1000 // in millisec -- 60000 (60 sec) max 
#define LOG_INTERVAL_REPEAT 10 // number of times to repeat BASE

//battery
#define BATTERYPIN A3

//RTC
RTC_DS3231 RTC;

//sd card and filename
const int chipSelect = 7;    
int SDpower = 5;
int sensorPower = 4;

char filename[] = "LOGGER00.csv";
File dataFile;
String fileHeader = "#DATETIME,RTC_TEMP_C,TEMP_C,HUMID_RH,CO2_PPM";

//variables for MHZ14 CO2 sensor
SoftwareSerial mhz14Serial(6, 8); // RX, TX
const byte mhz14_cmd[9] = {0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79};


unsigned long mhz14_read(){
    unsigned long dataHigh, dataLow, ppm;
    byte resp[9] = {0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80};
    //bool have_sync = false;
    //PING CO2, READ RESPONSE, GET READINGS AND CONVERT TO PPM
    mhz14Serial.write(mhz14_cmd,9);
    mhz14Serial.readBytes((char*)resp, 9);
    byte start=0;
    //Serial.print("[");
    for(byte i=0;i<9;i++){
      if(resp[i] == 0xFF) {
        start=i;
      }
      //Serial.print(resp[i]);
      //Serial.print(",");
    }
    //Serial.print("]");
    //if(have_sync)
    if(true)
    {
      //read out the next 8 bytes and decode
      //mhz14Serial.readBytes((char*)resp, 8);
      
      //dataHigh = (unsigned long) resp[1];
      //dataLow = (unsigned long) resp[2];
      dataHigh = (unsigned long) resp[(start+2)%9];
      dataLow = (unsigned long) resp[(start+3)%9];
      ppm = (256*dataHigh)+dataLow;
    } else {ppm = 0;} //failed to read data frame
    
    return ppm;
}


int interruptPin = 0; //corresponds to D2

void setup()
{
   if (debug==1){
    Serial.begin(9600);
  } 
      pinMode(led, OUTPUT);
      
      //turn on SD card
      pinMode(SDpower,OUTPUT);
      digitalWrite(SDpower,LOW);
      
      //initialize the SD card  
  if (debug==1){
    Serial.println();
    Serial.print("Initializing SD card...");
  }
  pinMode(SS, OUTPUT);
  
  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {  

     if (debug==1){
      Serial.println("Card failed, or not present");
    }
      
    for (int j=0;j<100;j++) {
        digitalWrite(led, LOW);
        delay(100);
        digitalWrite(led, HIGH);
         delay(100);
  }
  digitalWrite(led, LOW);
  
   
    // don't do anything more:
    while (1) ;
  }

  if (debug==1) {
    Serial.println("card initialized.");
  }
  
  for (uint8_t i = 0; i < 100; i++) {
    filename[6] = i/10 + '0';
    filename[7] = i%10 + '0';
    if (! SD.exists(filename)) {
      // only open a new file if it doesn't exist
      if (debug==1) {
        Serial.print("Writing to file: " );
        Serial.println(filename);
      }
      dataFile = SD.open(filename, FILE_WRITE);
      dataFile.println(fileHeader);
      dataFile.close();
      break;  // leave the loop!
    }
  }  
      
     // for i2c for RTC
  Wire.begin();
  RTC.begin();   
      
    // check on the RTC
  if (! RTC.isrunning()) {
    if (debug==1){
      Serial.println("RTC is NOT running!");
    }
      // following line sets the RTC to the date & time this sketch was compiled
    RTC.adjust(DateTime(__DATE__, __TIME__));
  }
  
  DateTime now = RTC.now();
  DateTime compiled = DateTime(__DATE__, __TIME__);
  if (now.unixtime() < compiled.unixtime()) {
    if (debug==1) {
    Serial.println("RTC is older than compile time! Updating");
    }
    RTC.adjust(DateTime(__DATE__, __TIME__));
  }
  if (debug==1) {
    Serial.println();
    Serial.println(fileHeader);
  }
  
  //set up soft serial port for CO2 sensor
  mhz14Serial.begin(9600);
  mhz14Serial.setTimeout(2000);
  //show that we're working
  if (debug==0) {
    for (int j=0;j<4;j++) {
      digitalWrite(led, LOW);
      delay(1000);
      digitalWrite(led, HIGH);
      delay(1000);
    }
  
   for (int j=0;j<3;j++) {
     digitalWrite(led, LOW);
     delay(500);
     digitalWrite(led, HIGH);
     delay(500);
   }
   digitalWrite(led, LOW);
   delay(1000);    
  }     
}

void loop()
{
  uint8_t i;
  float average;
  
  

   //get the time
  DateTime now = RTC.now();
  long unixNow = now.unixtime();
  
  // Onboard temp from the RTC
  float rtcTemp = RTC.getTempAsFloat();
  
  // temperature ---------------------------------------------
  float shtTemp = SHT2x.GetTemperature();
  
  // humidity-------------------------------------------------
  float shtHumid = SHT2x.GetHumidity();
  
  //CO2
  unsigned long co2PPM = mhz14_read();
  
  // Get the battery level
  int batteryLevel = analogRead(BATTERYPIN);

  // make a string for assembling the data to log:
  String dataString = "";
  

  // dataString += String(unixNow);
  dataString += now.unixtime();
  dataString += ",";
  dataString += now.year();
  dataString += "-";
  dataString += padInt(now.month(), 2);
  dataString += "-";
  dataString += padInt(now.day(), 2);
  dataString += " ";
  dataString += padInt(now.hour(), 2);
  dataString += ":";
  dataString += padInt(now.minute(), 2);
  dataString += ":";
  dataString += padInt(now.second(), 2);
  dataString += ",";
  char buffer[10];
  dataString += dtostrf(rtcTemp, 5, 2, buffer);
  dataString += ",";
  dataString += dtostrf(shtTemp,5,2, buffer);
  dataString += ",";
  dataString += dtostrf(shtHumid,5,2,buffer);
  dataString += ",";
  dataString += String(co2PPM);
/*  dataString += ",";*/
/*  dataString += String(batteryLevel);*/

  // Open up the file we're going to log to!
  dataFile = SD.open(filename, FILE_WRITE);
  if (!dataFile) {
    if (debug==1){
      Serial.print("Error opening file:");
      Serial.println(filename);
    }
    
    // Wait forever since we cant write data
    while (1) ;
  }
  
  digitalWrite(led, HIGH);
  delay(30);
  
  // Write the string to the card
  dataFile.println(dataString);
  dataFile.close();
  
  digitalWrite(led,LOW);
  
  if (debug==1) {
    Serial.println(dataString);
  }
  
// go to sleep!
   
  if (debug==0) {
    for (int k=0;k<LOG_INTERVAL_REPEAT;k++) {
      Sleepy::loseSomeTime(LOG_INTERVAL_BASE); //-- will interfere with serial, so don't use when debugging 
    }
  } else {
      for (int k=0;k<LOG_INTERVAL_REPEAT;k++) {
        delay (LOG_INTERVAL_BASE); // use when debugging -- loseSomeTime does goofy things w/ serial
      }
  }
}
  
String padInt(int x, int pad) {
  String strInt = String(x);
  
  String str = "";
  
  if (strInt.length() >= pad) {
    return strInt;
  }
  
  for (int i=0; i < (pad-strInt.length()); i++) {
    str += "0";
  }
  
  str += strInt;
  
  return str;
}

String int2string(int x) {
  // formats an integer as a string assuming x is in 1/100ths
  String str = String(x);
  int strLen = str.length();
  if (strLen <= 2) {
    str = "0." + str;
  } else if (strLen <= 3) {
    str = str.substring(0, 1) + "." + str.substring(1);
  } else if (strLen <= 4) {
    str = str.substring(0, 2) + "." + str.substring(2);
  } else {
    str = "-9999";
  }
  
  return str;
}

ISR(WDT_vect) { Sleepy::watchdogEvent(); }
