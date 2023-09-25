
import time
from wifi import Connect_wifi
from mqtt import *



ssid = "LMTX-PE"
pwd  = "962464@LMTX.com"

'''
ssid = "WIFI_B5ED"
pwd  = "1234567890"
'''
'''
ssid = "WW"
pwd  = "12345678"
'''
import machine
from machine import Pin

PSB_SELECT	   = 1
PSB_L3		   = 2
PSB_R3		   = 3
PSB_START	   = 4
PSB_PAD_UP	   = 5
PSB_PAD_RIGHT  = 6
PSB_PAD_DOWN   = 7
PSB_PAD_LEFT   = 8
PSB_L2		   = 9
PSB_R2		   = 10
PSB_L1		   = 11
PSB_R1		   = 12
PSB_GREEN	   = 13
PSB_RED		   = 14
PSB_BLUE	   = 15
PSB_PINK	   = 16
PSB_TRIANGLE   = 13
PSB_CIRCLE	   = 14
PSB_CROSS	   = 15
PSB_SQUARE	   = 26
PSS_RX = 5				  #x 
PSS_RY = 6
PSS_LX = 7
PSS_LY = 8

mask=[
	PSB_SELECT,
		PSB_L3,
		PSB_R3 ,
		PSB_START,
		PSB_PAD_UP,
		PSB_PAD_RIGHT,
		PSB_PAD_DOWN,
		PSB_PAD_LEFT,
		PSB_L2,
		PSB_R2,
		PSB_L1,
		PSB_R1 ,
		PSB_GREEN,
		PSB_RED,
		PSB_BLUE,
		PSB_PINK]
comd=[0x01,0x42]
data=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

class PS2KEY:
	#使用定义： PS2KEY('X18','X19','X20','X21')
	def __init__(self,_di,_do,_cs,_clk):
		
		self.di=Pin(_di,Pin.IN,Pin.PULL_DOWN)
		self.do=Pin(_do,Pin.OUT)
		self.cs=Pin(_cs,Pin.OUT)
		self.clk=Pin(_clk,Pin.OUT)

		self.ps2_init()
		self.ps2_red()
	
	def ps2_init(self):
		self.clk.value(1)
		self.do.value(1)
		time.sleep_ms(10)
		
	def ps2_cmd(self,cmd):
		global data
		data[1]=0
		for ref in (1,2,4,8,16,32,64,128):
		  if ( ref & cmd):
		   self.do.value(1)
		  else:
		   self.do.value(0)
		  self.clk.value(1)
		  time.sleep_us(10)
		  self.clk.value(0)
		  time.sleep_us(10)
		  self.clk.value(1)
		  if(self.di.value()==1):
		   data[1]=ref|data[1]
		   
	def ps2_red(self):
		global data
		global comd
		self.cs.value(0)
		self.ps2_cmd(comd[0])
		self.ps2_cmd(comd[1])
		self.cs.value(1)
		if(data[1]==57):
		  return 0#red light
		else:
		  return 1#not red
		  
	def ps2_read(self):
		global data
		global comd
		byte=0
		ref=0x01
		self.cs.value(0)
		self.ps2_cmd(comd[0])
		self.ps2_cmd(comd[1])
		for byte in (2,3,4,5,6,7,8):
		  for ref in (1,2,4,8,16,32,64,128):
		   self.clk.value(1)
		   self.clk.value(0)
		   time.sleep_us(10)
		   self.clk.value(1)
		   if(self.di.value()==1):
			data[byte]= ref|data[byte]
		  time.sleep_us(10)
		self.cs.value(1)
		
	def ps2_clear(self):#ok
		global data
		for i in range(0,9,1):
		  data[i]=0
	
	#获取摇杆电位值（0-255模拟量）
	def ps2_andata(self,button):
		global data
		return data[button]
	
	#获取按键值
	def ps2_key(self):
		global data
		global mask
		self.ps2_clear()
		self.ps2_read()
		handkey=(data[4]<<8)|data[3]
		for index in (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15):
		  if (( handkey&(1<<(mask[index]-1)))==0):
		   return index+2
		return 0

while (True):
    Connect_wifi(ssid, pwd)
    MQTT_Init()
    
    key_temp = 0
    
    while True:
        ps=PS2KEY(4,16,17,5)
        key = ps.ps2_key() # 获取按键值key
        if key is not key_temp:
            MQTT_SendMessage('{"key":"%d"}'%key)
            key_temp = key
            print(key)
            

    

    
               

