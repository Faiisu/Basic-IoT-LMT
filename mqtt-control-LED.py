import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# --- CONFIGURATION ---
WIFI_SSID = "Faiisu"
WIFI_PASSWORD = "69537873"

# HiveMQ Public Broker Details
MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "ESP32_Client_Unique_ID_123_idk"
MQTT_TOPIC = "faiisu/led_control123"

# Pin Setup
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
    
def sub_cb(topic, msg):
    """Callback function that runs when a message is received"""
    print((topic, msg))
    command = msg.decode('utf-8')
    
    if command == "test":
        print("receive MQTT message")
        led.toggle()

    if command == "LED1": led1.toggle()
    if command == "LED2": led2.toggle()
    
    if command == "BOTH":
        led1.toggle()
        led2.toggle()
        
    if command == "shutdown":
        led1.value(0)
        led2.value(0)
    return 0
    

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


# --- MAIN EXECUTION ---

connect_wifi()

client = connect_mqtt(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_TOPIC)

if client:
    led_test.value(1)
    try:
        while True:
            # Check for new messages (non-blocking)
            client.check_msg()
            time.sleep(0.1) 
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()
    except Exception as e:
        print(f"Error in main loop: {e}")
        # Ideally, add logic here to reconnect if Wi-Fi/MQTT drops
else:
    print("Could not start MQTT client.")