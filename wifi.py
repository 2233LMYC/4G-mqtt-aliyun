import network,time
from led import led

def Connect_wifi(ssid,pwd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, pwd)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    for i in range(10):
        led.value(not led.value())
        time.sleep_ms(100)
    led.value(1)
    print("WIFI connected")
