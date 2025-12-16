import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

WIFI_SSID = "Faiisu"
WIFI_PASSWORD = "69537873"

MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "ESP32_Client_Unique_ID_123_idk"
MQTT_TOPIC = "faiisu/led_control123"

led_test = Pin(2,Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print('.', end='')
    print('\nWi-Fi Connected:', wlan.ifconfig())
    
def sub_cb(topic, msg):
    print((topic, msg))
    command = msg.decode('utf-8')
    

def connect_mqtt(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_TOPIC):
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
        client.connect()
        client.set_callback(sub_cb)
        client.subscribe(MQTT_TOPIC)
        print(f"Connected to MQTT Broker: {MQTT_BROKER}")
        print(f"Subscribed to Topic: {MQTT_TOPIC}")
        return client
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")
        return 0


led_test.value(0)
connect_wifi()
client = connect_mqtt(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_TOPIC)

if client:
    led_test.value(1)
    while True:
        client.check_msg()
        time.sleep(0.1) 
else:
    print("Could not start MQTT client.")

