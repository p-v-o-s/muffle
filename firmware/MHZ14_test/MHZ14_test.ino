//MH-Z14 CO2 Module from Zhengzhou Winsen Electronics Technology Co., Ltd
/****************************************************/
#include <SoftwareSerial.h>
//using softserial to send/recieve data over analog pins 0 & 1
//SoftwareSerial mySerial(A0, A1); // RX, TX respectively
#define calibrationTime 600 //warm up time for C02 sensor (3min = 180sec)
//VARIABLES
byte cmd[9] = {0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79};
char response[9];
unsigned long time;

SoftwareSerial mySerial(A0, A1); // RX, TX

//////////////////////////////////////////////////////////// SETUP
void setup() {
    //sdCardSetup();//sdFormatter setup
    Serial.begin(9600);
    mySerial.begin(9600);
}
////////////////////////////////////////////////////////////END SETUP
void loop()
{
    time = millis(); //1s = 1000
    //PING CO2, READ RESPONSE, GET READINGS AND CONVERT TO PPM
    mySerial.write(cmd,9);
    mySerial.readBytes(response, 9);
    int responseHigh = (int) response[2];
    int responseLow = (int) response[3];
    int ppm = (256*responseHigh)+responseLow;
    Serial.println(response);
    Serial.println(ppm);
    delay(1000);
}
