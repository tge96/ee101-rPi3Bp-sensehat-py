from sense_hat import SenseHat
import time
import requests # sudo apt-get install python-requests
import serial

ser = serial.Serial("/dev/serial0")

EE101_SYNC = 0x50
EE101_TEXT_TYPE = 0x00
EE101_VALUE_TYPE = 0x80
EE101_LABEL = 0x08

def EE101Text(channel, text):
    ser.write(bytes([(int(channel) & 0x07) | EE101_SYNC | EE101_TEXT_TYPE]))
    ser.write(text.encode())
    ser.write(bytes([0]))
    
def EE101Value(channel, value):
    ser.write(bytes([(int(channel) & 0x07) | EE101_SYNC | EE101_VALUE_TYPE]))
    ser.write(bytes([(int(value >> 24))]))
    ser.write(bytes([(int(value >> 16))]))
    ser.write(bytes([(int(value >> 8))]))
    ser.write(bytes([(int(value) & 0xFF)]))

def EE101TextLabel(channel, label):
    ser.write(bytes([(int(channel) & 0x07) | EE101_SYNC | EE101_TEXT_TYPE | EE101_LABEL]))
    ser.write(label.encode())
    ser.write(bytes([0]))

def EE101ValueLabel(channel, label):
    ser.write(bytes([(int(channel) & 0x07) | EE101_SYNC | EE101_VALUE_TYPE | EE101_LABEL]))
    ser.write(label.encode())
    ser.write(bytes([0]))
    
sense = SenseHat()

def readings():
    t = sense.get_temperature() * (9/5) + 32 # convert to degrees F
    h = sense.get_humidity()
    p = sense.get_pressure() / 33.864 # convert to inHg (inches of mercury)

    EE101Value(0,int(round(t)))
    EE101Value(1,int(round(h)))
    EE101Value(2,int(round(p)))
    
    t = str(round(t, 1)) # convert to string
    h = str(round(h, 1))
    p = str(round(p, 1))
    url = 'https://dweet.io/dweet/for/shxyz?' + 'temperature=' + t + '&humidity=' + h + '&pressure=' + p
    r = requests.post(url) # to view point browser to https://dweet.io/follow/shxyz
    
    mytemp = 'Temperature (F):' + t
    print(mytemp)
    myhumi = 'Humidity (%):' + h
    print(myhumi)
    mypress = 'Pressure (inHg):' + p
    print(mypress)
    mytime = 'Readings recorded at ' + time.strftime("%H:%M:%S", time.localtime())
    print(mytime)
    
    EE101Text(0,mytemp)
    EE101Text(1,myhumi)    
    EE101Text(2,mypress)
    EE101Text(3,mytime)
    
try:

    print("Press CTL+C to exit program")

    for x in "EE101 Firmware Debugger":
        EE101TextLabel(0, "Temperature")
        EE101TextLabel(1, "Humidity")
        EE101TextLabel(2, "Pressure")
        EE101TextLabel(3, "Timestamp")
        EE101TextLabel(4, "Label Creator")
        mylabel = 'for loop character:' + x
        EE101Text(4, mylabel)
        EE101ValueLabel(0, "Temperature")
        EE101ValueLabel(1, "Humidity")
        EE101ValueLabel(2, "Pressure")
        EE101ValueLabel(3, "Pitch")
        EE101ValueLabel(4, "Yaw")
        EE101ValueLabel(5, "Roll")

    while True:
        
        readings()
        #msg = "Temp= %s, Press=%s, Humi=%s" %(t,p,h)
        #sense.show_message(msg, scroll_speed=0.05)
        time.sleep(10)

        pitch, roll, yaw = sense.get_orientation().values()
        print("pitch=%s, roll=%s, yaw=%s" % (int(round(pitch)),int(round(yaw)),int(round(roll))))
        EE101Value(3, int(round(pitch)))
        EE101Value(4, int(round(yaw)))
        EE101Value(5, int(round(roll)))
        
except KeyboardInterrupt:
    print("Exiting Program")

except:
    print("Error Occurs, Exiting Program")

finally:
    ser.close()
pass
   
