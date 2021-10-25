from platform import python_branch
from tkinter import *
from tkinter.ttk import *
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt

onLed = 0
onFan = 0
onRain = 0
Connected = False
host = "mqtt.sefvi.com"
port = 8888
log_mqtt = "test/log_mqtt"
app_esp_led = "test/app_esp/led"
app_esp_fan = "test/app_esp/fan"
app_esp_rain = "test/app_esp/rain"
app_esp_time_led = "test/app_esp/time_led"
app_esp_time_fan = "test/app_esp/time_fan"
app_esp_time_rain = "test/app_esp/time_rain"
app_esp_set = "test/app_esp/set"
esp_app_dht = "test/esp_app/dht"
esp_app_sttOff =  "test/esp_app/sttoff"
sttoff = ''

class Example(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()
    def initUI(self):
        self.parent.title("dashboard")
        self.pack(fill=BOTH, expand=True)
        
        client = self.connect_mqtt()
        client.loop_start()
        client.subscribe(esp_app_dht)
        client.subscribe(esp_app_sttOff)
    #define switch button
        on = PhotoImage(file="on.png")
        off = PhotoImage(file="off.png")

        def switchForLed():
            global onLed
            if onLed:
                btn_led.config(image=off)
                client.publish(app_esp_led,"0")
                onLed=0
            else:
                btn_led.config(image=on)
                client.publish(app_esp_led,"1")
                onLed=1
        def switchForFan():
            global onFan
            if onFan:
                btn_fan.config(image=off)
                client.publish(app_esp_fan,"0")
                onFan=0
            else:
                btn_fan.config(image=on)
                client.publish(app_esp_fan,"1")
                onFan=1
        def switchForRain():
            global onRain
            if onRain :
                btn_rain.config(image=off)
                client.publish(app_esp_rain,"0")
                onRain=0
            else:
                btn_rain.config(image=on)
                client.publish(app_esp_rain,"1")
                onRain=1
        def btnLed():
            #global onLed
            #btn_led.config(image=on)
            hour = led_hour.get()
            minute = led_minute.get()
            secons = led_secons.get()
            if len(hour) == 0: hour = 0
            else: hour = int(hour)
            if len(minute) == 0: minute = 0
            else: minute = int(minute)
            if len(secons) == 0: secons = 0
            else: secons = int(secons)
            res = hour*60*60 + minute*60 + secons
            client.publish(app_esp_time_led, str(res))
            lb_edit.config(text=res)
            #onLed = 1
        def btnFan():
            #global onFan
            #btn_fan.config(image=on)
            hour = fan_hour.get()
            minute = fan_minute.get()
            secons = fan_secons.get()
            if len(hour) == 0: hour = 0
            else: hour = int(hour)
            if len(minute) == 0: minute = 0
            else: minute = int(minute)
            if len(secons) == 0: secons = 0
            else: secons = int(secons)
            res = hour*60*60 + minute*60 + secons
            client.publish(app_esp_time_fan, str(res))
            lb_edit.config(text=res)
            #onFan = 1
        def btnRain():
            #global onRain
            #btn_rain.config(image=on)
            hour = rain_hour.get()
            minute = rain_minute.get()
            secons = rain_secons.get()
            if len(hour) == 0: hour = 0
            else: hour = int(hour)
            if len(minute) == 0: minute = 0
            else: minute = int(minute)
            if len(secons) == 0: secons = 0
            else: secons = int(secons)
            res = hour*60*60 + minute*60 + secons
            client.publish(app_esp_time_rain, str(res))
            lb_edit.config(text=res)
            #onRain = 1
        def seclect():
            hum = str(vMin.get())
            tem = str(vMax.get())
            if len(hum) == 1:
                hum = '0'+hum
            if len(tem) ==1:
                tem = '0'+tem
            seclection = hum+','+tem
            label_sec.config(text = seclection)
            client.publish(app_esp_set,seclection)

        self.varStt = StringVar()
        
        #screen app
        frame_dht = Frame(self)
        frame_dht.pack(fill=X)
        
        self.varHum = StringVar()
        lb1 = Label(frame_dht, text="Status: ")
        lb1.pack(side=LEFT, padx=10, pady=15)
        lb2 = Label(frame_dht, text="dht",textvariable=self.varHum)
        lb2.pack(side=LEFT, padx=70, pady=15)

        frame_textBtn = Frame(self)
        frame_textBtn.pack(fill=X)
        lb_led = Label(frame_textBtn, text="Led")
        lb_fan = Label(frame_textBtn, text="Rain")
        lb_rain = Label(frame_textBtn, text="Fan")
        lb_led.pack(side=LEFT, padx=50, pady=0)
        lb_fan.pack(side=LEFT, padx=60, pady=0)
        lb_rain.pack(side=LEFT, padx=50, pady=0)

        frame_btn = Frame(self)
        frame_btn.pack(fill=X)
        btn_led = Button(frame_btn, image=off,command=switchForLed)
        btn_led.pack(side=LEFT, padx=11, pady=0)
        btn_fan = Button(frame_btn,image=off,command=switchForFan)
        btn_fan.pack(side=LEFT, padx=11, pady=0)
        btn_rain = Button(frame_btn, image=off,command=switchForRain)
        btn_rain.pack(side=LEFT, padx=11, pady=0)

        # hen gio
        frame_text = Frame(self)
        frame_text.pack(fill=X)
        lb_text = Label(frame_text, text="Enter the time (hh:mm:ss):")
        lb_text.pack(side=LEFT,padx=10, pady=10)
        lb_edit = Label(frame_text)
        lb_edit.pack(side=LEFT, padx=20)

        frame_inputTime = Frame(self)
        frame_inputTime.pack(fill=X,padx=10)
        led_text = Label(frame_inputTime, text="Time Led: ")
        led_text.grid(column=0, row=0, padx=5)
        led_hour = Entry(frame_inputTime, width=3)
        led_hour.grid(column=1,row=0)
        lb_inpLed1 = Label(frame_inputTime, text=":")
        lb_inpLed1.grid(column=2, row=0)
        led_minute = Entry(frame_inputTime, width=3)
        led_minute.grid(column=3, row=0,padx=1)
        lb_inpLed2 = Label(frame_inputTime, text=":")
        lb_inpLed2.grid(column=4, row=0)
        led_secons = Entry(frame_inputTime, width=3)
        led_secons.grid(column=5, row=0)
        btn_inpLed = Button(frame_inputTime, text="accept", command=btnLed)
        btn_inpLed.grid(column=6, row=0,padx=20)

        fan_text = Label(frame_inputTime, text="Time Fan: ")
        fan_text.grid(column=0, row=1, padx=5)
        fan_hour = Entry(frame_inputTime, width=3)
        fan_hour.grid(column=1,row=1)
        lb_inpFan1 = Label(frame_inputTime, text=":")
        lb_inpFan1.grid(column=2, row=1)
        fan_minute = Entry(frame_inputTime, width=3)
        fan_minute.grid(column=3, row=1,padx=1)
        lb_inpFan2 = Label(frame_inputTime, text=":")
        lb_inpFan2.grid(column=4, row=1)
        fan_secons = Entry(frame_inputTime, width=3)
        fan_secons.grid(column=5, row=1)
        btn_inpFan = Button(frame_inputTime, text="accept", command=btnFan)
        btn_inpFan.grid(column=6, row=1,padx=20)

        rain_text = Label(frame_inputTime, text="Time Rain: ")
        rain_text.grid(column=0, row=2, padx=5)
        rain_hour = Entry(frame_inputTime, width=3)
        rain_hour.grid(column=1,row=2)
        lb_inpRain1 = Label(frame_inputTime, text=":")
        lb_inpRain1.grid(column=2, row=2)
        rain_minute = Entry(frame_inputTime, width=3)
        rain_minute.grid(column=3, row=2,padx=1)
        lb_inpRain2 = Label(frame_inputTime, text=":")
        lb_inpRain2.grid(column=4, row=2)
        rain_secons = Entry(frame_inputTime, width=3)
        rain_secons.grid(column=5, row=2)
        btn_inpRain = Button(frame_inputTime, text="accept", command=btnRain)
        btn_inpRain.grid(column=6, row=2,padx=20)

        #set min max
        frame_min = Frame(self)
        frame_min.pack(fill=X)
        label_min = Label(frame_min, text= "Humidity:",width=15)
        label_min.pack(side=LEFT, padx=5, pady=15)
        vMin = IntVar()
        scale_min = Scale(frame_min, variable=vMin, from_=0, to=99, command=self.onScaleMin)
        scale_min.pack(side=LEFT, padx=5,expand=True)
        self.varMin = IntVar()
        lable1 = Label(frame_min, text=0, textvariable=self.varMin)
        lable1.pack(side=LEFT, padx=10)
        donVi = Label(frame_min, text='%')
        donVi.pack(side=LEFT)

        #frame max humidity
        frame_max = Frame(self)
        frame_max.pack(fill=X)
        label_max = Label(frame_max, text= "Temperature:",width=15)
        label_max.pack(side=LEFT, padx=5, pady=5)
        vMax = IntVar()
        scale_max= Scale(frame_max,variable=vMax, from_=0, to=50, command=self.onScaleMax)
        scale_max.pack(side=LEFT, padx=15,expand=True)
        self.varMax = IntVar()
        lable2 = Label(frame_max, text=0, textvariable=self.varMax)
        lable2.pack(side=LEFT, padx=10)
        donVi = Label(frame_max, text='*C')
        donVi.pack(side=LEFT)

        #button set auto
        btn_ok = Button(self, text="accept", command= seclect)
        btn_ok.place(x=300,y=320)
        label_sec = Label()
        label_sec.pack()
     
    #lay gia tri val tu scale
    def onScaleMin(self, val):
        v = int(float(val))
        self.varMin.set(v)      
    def onScaleMax(self, val):
        v = int(float(val))
        self.varMax.set(v)

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        def on_mess(client, userdata, message):
            load = message.topic
            if load == esp_app_sttOff:
                stt = str(message.payload.decode("utf-8"))
                self.varStt.set(stt)
                sttoff = message.payload
               
            elif load == esp_app_dht:
                humNow = str(message.payload.decode("utf-8"))
                self.varHum.set(humNow)
                print(humNow)
    
        client = mqtt_client.Client()
        #client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.on_message = on_mess
        client.connect("mqtt.sefvi.com", 8888, 60)
        return client
        
root = Tk()
root.geometry('400x380')
app = Example(root)
root.mainloop()