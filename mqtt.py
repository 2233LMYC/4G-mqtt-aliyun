
from umqtt.simple import MQTTClient
import time
from led import led
from machine import Timer
import json


SERVER = 'iot-06z00ieryw2crbw.mqtt.iothub.aliyuncs.com'  # mqttHostUrl
CLIENT_ID = "k08abBUtNji.ESP32|securemode=2,signmethod=hmacsha256,timestamp=1695213017785|"  # clientId
username = 'ESP32&k08abBUtNji' #username
password = '3fabee8ebe3fb9cc84fe690bc9066b6ed1f17faa5c0f2f70676ae997289fb7ca'  #密码
publish_TOPIC = '/k08abBUtNji/ESP32/user/update'
subscribe_TOPIC = '/k08abBUtNji/ESP32/user/get'
#---以上的参数值都需要根据自己的环境修改-----------------------------------------------


client = None


#接收的回调函数
def sub_cb(topic, msg):
    global led
    msg = json.loads(msg)
    print(msg)
    if msg['type'] =='ON':
        led.value(1)
        print('led ON')
    if msg['type'] =='OFF':
        led.value(0)
        print('led OFF')
        
#MQTT初始化
def MQTT_Init():
    global client
    global led
    
    client = MQTTClient(CLIENT_ID, SERVER, 0, username, password, 60)  # create a mqtt client
    print('client:%s' % str(client))
    led.value(1)
    client.set_callback(sub_cb)  # set callback
    client.connect()  # connect mqtt
    client.subscribe(subscribe_TOPIC)  # client subscribes to a topic


#发送数据
def MQTT_SendMessage(message):
    global client
    client.publish(topic=publish_TOPIC, msg=message, retain=False, qos=0)



               

