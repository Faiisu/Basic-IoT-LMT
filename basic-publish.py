import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

WIFI_SSID = "Faiisu"
WIFI_PASSWORD = "69537873"

MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "ESP32_Client_Unique_ID_123_idk"
MQTT_TOPIC = "faiisu/led_control123"

led_test = Pin(2, Pin.OUT) 
led1 = Pin(4, Pin.OUT)
led2 = Pin(16, Pin.OUT)


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
    

def connect_mqtt(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_TOPIC):
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
        client.connect()
        print(f"Connected to MQTT Broker: {MQTT_BROKER}")
        return client
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")
        return 0


# --- MAIN EXECUTION ---

connect_wifi()
client = connect_mqtt(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_TOPIC)

if client:
    led_test.value(1)
    while True:
        client.publish(MQTT_TOPIC, "Hello from ESP32")        
        time.sleep(1)

else:
    print("Could not start MQTT client.")


