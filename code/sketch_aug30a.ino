#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 12
#define PIN2 11
#define NUMPIXELS (8*3)
#define BRIGHTNESS 180

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel strip2 = Adafruit_NeoPixel(NUMPIXELS, PIN2, NEO_GRB + NEO_KHZ800);
uint32_t firstPixelHue = 0;

void setup() {
  Serial.begin(115200);
  strip.setBrightness(BRIGHTNESS);
  strip2.setBrightness(BRIGHTNESS);
  strip.begin();
  strip2.begin();
  strip.show();
  strip2.show();
}
int color[5] = {0,0,0,0,0};
int zone[3] = {0,8,16};

unsigned long millisTime = millis();
unsigned long old_millisTime = millis();
void loop() {
  unsigned long millisTime = millis();
  if(Serial.available()>0){
      int ord = str_to_int(Serial.readStringUntil('\n'));
      if(ord){
        if(color[0]<=2){
          strip.setPixelColor((color[0]*8)+color[1],strip.Color(color[2],color[3],color[4]));
          strip.show();
        }
        else{
          strip2.setPixelColor(((color[0]-3)*8)+color[1],strip2.Color(color[2],color[3],color[4]));
          strip2.show();
        }
        old_millisTime = millisTime;
      }
    }

  if(millisTime-old_millisTime > 10000){
    whiteOverRainbow();
    old_millisTime = millisTime;
  }

}
void whiteOverRainbow() {
    for(int i=0; i<strip.numPixels(); i++) {
        int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
        strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
        strip2.setPixelColor(i, strip2.gamma32(strip2.ColorHSV(pixelHue)));
    }
    strip.show();
    strip2.show();
    firstPixelHue += 10;
  
}


int str_to_int(String data){
  Serial.println(data);
  if(data[0] == '('){
    int ID_data = data.indexOf(",",1);
    int division_data = data.indexOf(",",ID_data+1);
    int first_data = data.indexOf(",",division_data+1);
    int second_data = data.indexOf(",",first_data+1);
    int third_data = data.length()-1;
    
    color[0] = data.substring(1,ID_data).toInt();
    color[1] = data.substring(ID_data+1,division_data).toInt();
    color[2] = data.substring(division_data+1,first_data).toInt();
    color[3] = data.substring(first_data+1, second_data).toInt();
    color[4] = data.substring(second_data+1, third_data).toInt();
    
    return 1;
  }
  return -1;
}
