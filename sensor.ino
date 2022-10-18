#include <SimpleDHT.h>

SimpleDHT22 dht22(8);
int MicVolume = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {

  //TEMPERATURA E UMIDITà
 
  float temp = 0;
  float hum = 0;

  dht22.read2(&temp, &hum, NULL);

  Serial.print((float)temp);
  Serial.print(" °C ");
  Serial.print((float)hum);
  Serial.println(" H \n");
  delay (2000); 

  
  //SUONO

   MicVolume = (analogRead(1));
   Serial.println(abs(MicVolume - 256));
   delay(5);

}
