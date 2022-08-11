#client code for running in the background, reading CPU, disk usage and RAM usage and sending off via MQTT

from time import sleep, ctime
#from datetime import datetime
import paho.mqtt.client as mqtt
import psutil

MACHINE = "testbed"
SERVER = "192.168.50.72"


def life_monitor(): #read CPU and RAM
    #get CPU load
    area = "cpu"
    CPULOAD = psutil.cpu_percent(interval=1, percpu=False)
    CPULOAD = float(CPULOAD)
    CPULOAD = str(CPULOAD)
    print(CPULOAD)

    MESSAGE = (area + "-" + CPULOAD)
    mqtt_post(MESSAGE)

    #get memory load
    area = "mem"
    MEMLOAD = psutil.virtual_memory().percent
    MEMLOAD = float(MEMLOAD)
    MEMLOAD = str(MEMLOAD)
    print(MEMLOAD)

    MESSAGE = (area + "-" + MEMLOAD)
    mqtt_post(MESSAGE)

    #get disk usage
    area = "dsk"
    DISKUSE = psutil.disk_usage('/').percent
    DISKUSE = float(DISKUSE)
    DISKUSE = str(DISKUSE)
    print(DISKUSE)

    MESSAGE = (area + "-" + DISKUSE)
    mqtt_post(MESSAGE)

def mqtt_connection():
    global client
    global SERVER
    global MACHINE
    #variables for mqtt and making intial connection
    #broker_url = SERVER
    client = mqtt.Client(MACHINE)
    #try: #attempt intial connection
    #client.connect(broker_url, broker_port)
    client.connect(SERVER, port=1883)
    #except: #on error write log and close
    #    print("Error in MQTT connection")
    #    error_message("mqtt connection failed")

def mqtt_post(mpayload): #send to mqtt server
    #try:
        global MACHINE
        print("Posting message " + mpayload)
        mqtt_connection()
        print(MACHINE)
        client.publish(MACHINE, mpayload)
    #except:
    #    error_message("mqtt_post failed")

while True:
    life_monitor()
    sleep(5)