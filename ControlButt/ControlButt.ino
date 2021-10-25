#include <ESP8266WiFi.h>
#include <DHT.h>
#include <PubSubClient.h>

#define ssPin 2 // D4
#define rLed 5 // D1
#define rFan 4 // D2
#define rRain 16 // D0
#define ssid "KhanhHoi_Company"
#define pass "184khanhhoi"
//#define ssid "TP-Link_6A1C"
//#define pass "46522801"
#define server "mqtt.sefvi.com"
const uint16_t port = 8888;
#define log_mqtt "test/log_mqtt"
#define app_esp_led "test/app_esp/led"
#define app_esp_fan "test/app_esp/fan"
#define app_esp_rain "test/app_esp/rain"
#define app_esp_time_led "test/app_esp/time_led"
#define app_esp_time_fan "test/app_esp/time_fan"
#define app_esp_time_rain "test/app_esp/time_rain"
#define esp_app_dht "test/esp_app/dht"
#define esp_app_sttoff "test/esp_app/sttoff"
#define app_esp_set "test/app_esp/set"

DHT dht(ssPin, DHT22);

unsigned long timeMil = 0;
unsigned long timeRecLed;
unsigned long timeRecFan;
unsigned long timeRecRain;
int stt = 0;

char tempLed[10];
char tempFan[10];
char tempRain[10];
char tempSet[5];
String humi = "";
String tempe = "";
String setTimeLed = "";
int timeLed;
String setTimeFan = "";
int timeFan;
String setTimeRain = "";
int timeRain;
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  setup_wifi();
  dht.begin();
  pinMode(rLed, OUTPUT);
  pinMode(rFan, OUTPUT);
  pinMode(rRain, OUTPUT);
  client.setServer(server, port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int hum = dht.readHumidity();
  int temp = dht.readTemperature();
  if ((unsigned long) (millis() - timeMil) > 5000) {
    String out = String(hum) + "%_" + String(temp) + "*C";
    Serial.println(out);
    client.publish(esp_app_dht, out.c_str(), true);
    timeMil = millis();
  }
  if ((unsigned long)((timeRecLed + timeLed) - millis()) == 0) {
    digitalWrite(rLed, LOW);
    client.publish(esp_app_sttoff, "ledoff");
  }
  if ((unsigned long)((timeRecFan + timeFan) - millis()) == 0) {
    digitalWrite(rFan, LOW);
    client.publish(esp_app_sttoff, "fanoff");
  }
  if ((unsigned long)((timeRecRain + timeRain) - millis()) == 0) {
    digitalWrite(rRain, LOW);
    client.publish(esp_app_sttoff, "rainoff");
  }
  if(stt==1){
    if (hum < humi.toInt()){
      digitalWrite(rRain, HIGH);
    }else if (hum >= humi.toInt()){
      digitalWrite(rRain, LOW);
    }
    if(temp >= tempe.toInt()){
      digitalWrite(rFan, HIGH);
    }else if (temp <= tempe.toInt()){
      digitalWrite(rFan, LOW);
    }
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("wifi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  if (strcmp(topic, app_esp_led) == 0) {
    if (payload[0] == '1') {
      Serial.println("led on");
      digitalWrite(rLed, HIGH);
    } else if (payload[0] == '0') {
      Serial.println("led off");
      digitalWrite(rLed, LOW);
    }
  } else if (strcmp(topic, app_esp_fan) == 0) {
    stt = 0;
    if (payload[0] == '1') {
      Serial.println("fan on");
      digitalWrite(rFan, HIGH);
    } else if (payload[0] == '0') {
      Serial.println("fan off");
      digitalWrite(rFan, LOW);
    }
  } else if (strcmp(topic, app_esp_rain) == 0) {
    stt = 0;
    if (payload[0] == '1') {
      Serial.println("rain on");
      digitalWrite(rRain, HIGH);
    } else if (payload[0] == '0') {
      Serial.println("rain off");
      digitalWrite(rRain, LOW);
    }
  } else if (strcmp(topic, app_esp_time_led) == 0) {
    if (payload[0] > 0) {
      digitalWrite(rLed, HIGH);
    }
    int i;
    for( i = 0; i<length; i++){
      tempLed[i] = (char)payload[i];
    }
    tempLed[i]='\0';
    setTimeLed = String(tempLed);
    timeLed = setTimeLed.toInt() * 1000;
    timeRecLed = millis();
    Serial.println(setTimeLed);
    Serial.println(timeRecLed);
    Serial.println(timeLed);
    } else if (strcmp(topic, app_esp_time_fan) == 0) {
    stt = 0;
    if (payload[0] > 0) {
      digitalWrite(rFan, HIGH);
    }
    int i;
    for( i = 0; i<length; i++){
      tempFan[i] = (char)payload[i];
    }
    tempFan[i]='\0';
    setTimeFan = String(tempFan);
    timeFan = setTimeFan.toInt() * 1000;
    timeRecFan = millis();
    Serial.println(setTimeFan);
    Serial.println(timeRecFan);
    Serial.println(timeFan);
  } else if (strcmp(topic, app_esp_time_rain) == 0) {
    stt = 0;
    if (payload[0] > 0) {
      digitalWrite(rRain, HIGH);
    }
    int i;
    for( i = 0; i<length; i++){
      tempRain[i] = (char)payload[i];
    }
    tempRain[i]='\0';
    setTimeRain = String(tempRain);
    timeRain = setTimeRain.toInt() * 1000;
    timeRecRain = millis();
    Serial.println(setTimeRain);
    Serial.println(timeRecRain);
    Serial.println(timeRain);
  } else if (strcmp(topic, app_esp_set) == 0) {
    stt = 1;
    for (int i = 0; i < length; i++) {
      tempSet[i] = (char)payload[i];
      Serial.print(tempSet[i]);

    }
    humi = (String(tempSet[0]) + String(tempSet[1]));
    tempe = (String(tempSet[3]) + String(tempSet[4]));
    Serial.println(humi+" "+tempe);
    
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("esp8266Client")) {
      Serial.println("Connected");
      client.publish(log_mqtt, "reconnect success");
      client.subscribe(app_esp_led);
      client.subscribe(app_esp_fan);
      client.subscribe(app_esp_rain);
      client.subscribe(app_esp_time_led);
      client.subscribe(app_esp_time_fan);
      client.subscribe(app_esp_time_rain);
      client.subscribe(app_esp_set);
      Serial.println("subscribe success!");
    } else {
      Serial.print("failed, rc= ");
      Serial.println(client.state());
      Serial.println("try again in 5s");
      delay(5000);
    }
  }
}
