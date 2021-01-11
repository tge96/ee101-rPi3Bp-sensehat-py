from sense_hat import SenseHat
import time
import requests # sudo apt-get install python-requests
import serial

ser = serial.Serial("/dev/serial0")

def EE101Text(channel, text):
    EE101_SYNC = 0x50
    EE101_TEXT_TYPE = 0x00
    ser.write(bytes([(int(channel) & 0x07) | EE101_SYNC | EE101_TEXT_TYPE]))
    ser.write(text.encode())
    ser.write(bytes([0]))
    
def EE101Value(channel, value):
    EE101_SYNC = 0x50
    EE101_VALUE_TYPE = 0x80
    ser.write(bytes([(int(channel) & 0x07) | EE101_SYNC | EE101_VALUE_TYPE]))
    ser.write(bytes([(int(value >> 24))]))
    ser.write(bytes([(int(value >> 16))]))
    ser.write(bytes([(int(value >> 8))]))
    ser.write(bytes([(int(value) & 0xFF)]))
    
sense = SenseHat()

def readings():
    t = sense.get_temperature() * (9/5) + 32 # convert to degrees F
    p = sense.get_pressure() / 33.864 # convert to inHg (inches of mercury)
    h = sense.get_humidity()
    t = str(round(t, 0)) # convert to string
    p = str(round(p, 1))
    h = str(round(h, 1))
    url = 'https://dweet.io/dweet/for/shxyz?' + 'temperature=' + t + '&humidity=' + h + '&pressure=' + p
    r = requests.post(url) # to view point browser to https://dweet.io/follow/shxyz
    
    mytemp = 'Temperature (F):' + t
    print(mytemp)
    myhumi = 'Humidity (%):' + h
    print(myhumi)
    mypress = 'Pressure (inHg):' + p
    print(mypress)
    mytime = "Readings recorded at " + time.strftime("%H:%M:%S", time.localtime())
    print(mytime)
    
    EE101Text(0,mytemp)
    EE101Text(1,myhumi)    
    EE101Text(2,mypress)
    EE101Text(3,mytime)
    
try:

    print("Press CTL+C to exit program")

    while True:
        
        readings()
        #msg = "Temperature = %s, Pressure=%s, Humidity=%s" %(t,p,h)
        #sense.show_message(msg, scroll_speed=0.05)

        time.sleep(5)
        
except KeyboardInterrupt:
    print("Exiting Program")

except:
    print("Error Occurs, Exiting Program")

finally:
    ser.close()
pass
   
