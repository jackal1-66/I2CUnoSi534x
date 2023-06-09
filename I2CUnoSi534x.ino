#include <Wire.h>
#define SI5341 0x77 //depends on pins A0 A1, ranges from 74 to 77
#define SI5344 0x6B //depends on pins A0 A1, ranges from 68 to 6B

char rserial;
String t_reg, t_val, t_pag;
char *regstr, *valstr, *pagstr;
long reg, val, pag;
void setup() {
  Serial.begin(115200);  // put your setup code here, to run once:
  Serial.setTimeout(10);
  page(0x0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0)
    rserial = Serial.read();
  if(rserial == '1'){
    while (Serial.available()) 
      Serial.read();
    while(Serial.available() == 0){}
    t_pag = Serial.readStringUntil('\r');
    while(Serial.available() == 0){}
    t_reg = Serial.readStringUntil('\r');
    const char * tempag = t_pag.c_str();
    const char * temp = t_reg.c_str();  
    pag = strtoul(tempag, &pagstr,16);
    reg = strtoul(temp, &regstr,16);
    page(pag);
    //Serial.println(reg,HEX);
    //pgg = Serial.readStringUntil('\n');
    //while(Serial.available() > 0)
    //  reg = Serial.read();"      
    //print("Board revision is 0x");
    //uint16_t board = (read(0x03) << 8) | read(0x02);
    //Serial.println(read(board),HEX);
    Serial.println(read(reg),HEX);
  }
  else if(rserial == '0'){
    while (Serial.available())  //Necessary because python for some reason is sending random data after this
      Serial.read();
    while(Serial.available() == 0){}
    t_pag = Serial.readStringUntil('\r');  
    while(Serial.available() == 0){}
    t_reg = Serial.readStringUntil('\r');
    while(Serial.available() == 0){}
    t_val = Serial.readStringUntil('\r');
    const char * temp_reg = t_reg.c_str();  
    reg = strtoul(temp_reg, &regstr,16);
    const char * temp_val = t_val.c_str();  
    val = strtoul(temp_val, &valstr,16);
    const char * tempag = t_pag.c_str();
    pag = strtoul(tempag, &pagstr,16);
    page(pag);
    write(reg, val);
  }
  else if(rserial == '7'){
    while(Serial.available() == 0){}
    t_pag = Serial.readStringUntil('\r');  
    while(Serial.available() == 0){}
    t_reg = Serial.readStringUntil('\r');
    while(Serial.available() == 0){}
    t_val = Serial.readStringUntil('\r');
    const char * temp_reg = t_reg.c_str();  
    reg = strtoul(temp_reg, &regstr,16);
    const char * temp_val = t_val.c_str();  
    val = strtoul(temp_val, &valstr,16);
    const char * tempag = t_pag.c_str();
    pag = strtoul(tempag, &pagstr,16);
    page(pag);
    write(reg, val);
  }
  rserial = ' ';
  reg = 0;
  t_reg = ' ';
  pag = 0;
  t_pag = ' ';
  val = 0;
  t_val = ' ';
  delay(10);
  /*Wire.beginTransmission(SI5341);
  Wire.write(0x08);
  Wire.write(0x01);
  Wire.endTransmission();*/
}

void write(byte address, byte value){
  Wire.beginTransmission(SI5341);
  Wire.write(address);
  Wire.write(value);
  Wire.endTransmission();
}

void page(byte page){
  write(0x01,page);
}

byte read(byte address){
  Wire.beginTransmission(SI5341);
  Wire.write(address);
  Wire.endTransmission();
  Wire.requestFrom(SI5341, 1);
  char rval;
  while (Wire.available())
    rval = Wire.read();
  return rval;
}