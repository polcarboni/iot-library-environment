#include <SimpleDHT.h>

#define COMMUNICATION_TIME 5000
#define SOUND_TIME 25  

#define OUT_PIN 2
#define IN_PIN 4


SimpleDHT22 dht22(8);

int people_count;
int in_pressed;
int out_pressed;

unsigned long int cur_time;
unsigned long int humtemp_time;
unsigned long int sound_time;

int noise_level;
int sound_lev;

int sound_lev_0;
int sound_lev_1;
int sound_lev_2;
int sound_lev_3;

float temp;
float hum;

int pressed;
int counted;
int in_flag;
int out_flag;

void setup() {
  
  cur_time = 0;
  
  
  people_count = 0;
  
  pressed = 0;
  counted = 0;
  out_flag = 0;
  in_flag = 0;
  in_pressed = 0;
  out_pressed = 0;
  
  humtemp_time = 0;
  sound_time = 0;

  sound_lev_0 = 0;
  sound_lev_1 = 0;
  sound_lev_2 = 0;
  sound_lev_3 = 0;
  
  noise_level = 0;
  sound_lev = 0;
  temp = 0;
  hum = 0;


 

  pinMode(IN_PIN, INPUT);
  pinMode(OUT_PIN, INPUT);

 Serial.begin(9600);
}

void loop() {

//__________________________PEOPLE_COUNTING___________________________
    
 
  in_pressed = digitalRead(IN_PIN);
  out_pressed = digitalRead(OUT_PIN);

  
  if (in_pressed != 0 && pressed != 2) {
    pressed = 1;
  }
  
  if (out_pressed != 0 && pressed != 1) {
    pressed = 2;
  }

  if (pressed == 1 && in_pressed == 1) {
    in_flag = 1;
  }

  if (pressed == 2 && out_pressed == 1) {
    out_flag = 1;
  }

  if (out_flag == 1 && out_pressed == 0) {
    counted --;

    /*
    //Serial.print("USCITA REGISTRATA. TOTALE PRESENTI: ");
    Serial.print(counted);
    Serial.print("\n");
    */
    
    out_flag = 0;
    pressed = 0;
  }

   if (in_flag == 1 && in_pressed == 0) {
    counted ++;

    /*
    //Serial.print("ENTRATA REGISTRATA. TOTALE PRESENTI: ");
    Serial.print(counted);
    Serial.print("\n");
    */
    
    in_flag = 0;
    pressed = 0;
  }


  /* // LOGICA BOTTONI
    Serial.print(pressed);
    Serial.print(in_pressed);
    Serial.println(out_pressed);
  */
  


//_________________________HUMIDITY_AND_TEMPERATURE____________________
/*

//OVERFLOW (BASARE IL TIMER SU QUELLO PIÙ VELOCE DEL SUONO)

   if ((millis() - humtemp_time) > HUMTEMP_TIME) {
    Serial.println(humtemp_time);
    humtemp_time = millis();
    
    dht22.read2(&temp, &hum, NULL);

    Serial.print(millis());
    Serial.print("    ");
    Serial.println(humtemp_time);
   }
*/

//_________________________NOISE_LEVEL______________________________________

   
   if ((millis() - sound_time) > SOUND_TIME) {
    
    noise_level = (analogRead(1));
    sound_lev = abs(noise_level - 256);

    //Serial.println(sound_lev);
    

    if (sound_lev < 25) sound_lev_0 ++;
    else if (sound_lev >= 25 && sound_lev < 60 && in_pressed == 0 && out_pressed == 0) sound_lev_1 ++;
    else if (sound_lev >= 60 && sound_lev < 100 && in_pressed == 0 && out_pressed == 0) sound_lev_2 ++;   //bug sulla pressione del pulsante di ingresso
    else if (sound_lev >= 100 && in_pressed == 0 && out_pressed == 0) sound_lev_3 ++;   //bug sulla pressione del pulsante di ingresso
    
    
    sound_time = millis();

   }


//_________________________SERIAL_COMMUNICATION_+_HUMTEMP____________________________

  if ((millis()- cur_time) > COMMUNICATION_TIME) {
    
    dht22.read2(&temp, &hum, NULL);

    String hum_string = String(hum);
    String temp_string = String(temp);
    String counted_string = String(-counted);
    String lev0 = String(sound_lev_0);
    String lev1 = String(sound_lev_1);
    String lev2 = String(sound_lev_2);
    String lev3 = String(sound_lev_3);
    

    String output = hum_string + " %,  " + temp_string + "°C,  posti: " + counted_string + ",  Sounds: "
                      + lev0 + " " + lev1 + " " + lev2 + " " + " " + lev3;
    Serial.println(output);
    
      counted = 0;
      sound_lev_0 = 0;
      sound_lev_1 = 0;
      sound_lev_2 = 0;
      sound_lev_3 = 0;
  
    cur_time = millis();
  }
}
