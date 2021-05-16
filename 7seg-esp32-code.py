#***************************************
#** by    :   Mohammed Rashad         **
#**           Abdelmonuiem Bahaa      **
#**           Mohammed zaky           **
#**           Saed magdy              **
#**           Mohammed Roshdy         **
#**                                   **
#** date  :   1 Jan 2021              **
#** Title :   7 segment desplay v3.0  **
#***************************************
#***************************************


#modules and libraries 
#***************************************
from machine import Pin, Timer
import time
from time import sleep
import network
#***************************************

#wifi initialization as Access point interface
#***************************************
ssid     = '7segment controller'
password = '123456789'
ap       = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
while not ap.active():
    pass
print('network config:', ap.ifconfig())
#***************************************


# Configure the socket connection
# over TCP/IP
#***************************************
import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
s.listen(5)     # max of 5 socket connections
#***************************************



#7 segment and buttons objects creating
#***************************************
a   =Pin(23,Pin.OUT)
b   =Pin(22,Pin.OUT)
c   =Pin(21,Pin.OUT)
d   =Pin(19,Pin.OUT)
e   =Pin(18,Pin.OUT)
f   =Pin(5,Pin.OUT)
g   =Pin(17,Pin.OUT)
up  =Pin(16,Pin.IN,Pin.PULL_UP)
down=Pin(4,Pin.IN,Pin.PULL_UP)
rest=Pin(2,Pin.IN,Pin.PULL_DOWN)
#***************************************

#7segmant variables 
#***************************************
numm=0  
#          0                 1               2               3               4               5               6               7              8               9
num=[[1,1,1,1,1,1,0],[0,1,1,0,0,0,0],[1,1,0,1,1,0,1],[1,1,1,1,0,0,1],[0,1,1,0,0,1,1],[1,0,1,1,0,1,1],[1,0,1,1,1,1,1],[1,1,1,0,0,0,0],[1,1,1,1,1,1,1],[1,1,1,0,0,1,1]]     
#***************************************


#function to desplay any number in the 7 segment 
#***************************************
def desplay (number):
    for j in range(8):
        if j == 0 :   
            a.value(num[number][j])
        elif j == 1 :   
            b.value(num[number][j])
        elif j == 2 :   
            c.value(num[number][j])
        elif j == 3 :   
            d.value(num[number][j])
        elif j == 4 :   
            e.value(num[number][j])
        elif j == 5 :   
            f.value(num[number][j])
        elif j == 6 :   
            g.value(num[number][j])

#***************************************

#IRQ handlers for up down and reset
#***************************************
def funcup(timer):
    global numm
    global desplay
    sleep(0.25)
    if numm==9 :
        numm=0
    else:
        numm=numm+1
    desplay(numm)
    
def funcdown(timer):
    global numm
    global desplay
    sleep(0.25)
    if numm==0 :
        numm=0
    else:
        numm=numm-1
    desplay(numm)
    
def funcrest(timer):
    global numm
    global desplay
    sleep(0.25)
    numm=0
    desplay (numm)
    
#***************************************

#debounce functions for all three buttons
#***************************************    
def debounce(pin):
    # Start or replace a timer for 200ms, and trigger on_pressed.
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=funcup)
def debounce2(pin):
    # Start or replace a timer for 200ms, and trigger on_pressed.
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=funcdown)
def debounce3(pin):
    # Start or replace a timer for 200ms, and trigger on_pressed.
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=funcrest)

# Register a new hardware timer.
timer = Timer(0)   
#***************************************

#setting interrupt for the 3 buttons 
#***************************************
up.irq(debounce , Pin.IRQ_FALLING)
down.irq(debounce2 , Pin.IRQ_FALLING)
rest.irq(debounce3 , Pin.IRQ_RISING)
#***************************************


#get client connection 
#***************************************
conn, addr = s.accept()


#the code here running for ever 
#***************************************
while True :
#getting data from the application and response 
#***************************************
    while ap.isconnected():
        request    = conn.recv(1024)
        request    = str(request)
        upv        = request[2]
        print(upv)
        if upv=='u':
            sleep(0.5)
            if numm==9 :
                numm=0
            else :
                numm+=1
        elif upv=='d':
            sleep(0.5)
            if numm==0 :
                numm=0
            else :
                numm-=1
        elif upv=='r':
            sleep(0.5)
            numm=0
        elif upv=='x':
            sleep(0.5)
            pass
        else :
            sleep(0.5)
            numm=int(upv)
        
        conn.send(str(numm).encode())
        desplay(numm)
#***************************************
#***************************************
#***************************************
#***************************************
