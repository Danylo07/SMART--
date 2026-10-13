#!/usr/bin/env python3
import random, time, threading
import paho.mqtt.client as mqtt
class Simulator:
 def __init__(self):
  try: self.c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id="smart_home_simulator")
  except AttributeError: self.c=mqtt.Client(client_id="smart_home_simulator")
  self.s={"living_room_light":{"power":False,"brightness":50},"bedroom_light":{"power":False,"brightness":70},"kitchen_light":{"power":False,"brightness":60},"kitchen_dimmer":{"brightness":0},"thermostat":{"current_temp":21.0,"target_temp":22.0,"heating":False},"motion_detector":{"motion":False},"door_sensor":{"open":False},"smart_socket":{"power":False,"consumption":0}}
  self.lock=threading.RLock(); self.running=True
 def pub(self,t,v): self.c.publish(t,str(v),retain=True)
 def device(self,d):
  s=self.s[d]
  if d.endswith("_light"): self.pub(f"smarthome/{d}/state","ON" if s["power"] else "OFF"); self.pub(f"smarthome/{d}/brightness",s["brightness"])
  elif d=="kitchen_dimmer": self.pub("smarthome/kitchen_dimmer/brightness",s["brightness"])
  elif d=="thermostat":
   self.pub("smarthome/thermostat/current_temp",round(s["current_temp"],1)); self.pub("smarthome/thermostat/target_temp",s["target_temp"]); self.pub("smarthome/thermostat/heating","ON" if s["heating"] else "OFF")
  elif d=="motion_detector": self.pub("smarthome/motion_detector/state","ON" if s["motion"] else "OFF")
  elif d=="door_sensor": self.pub("smarthome/door_sensor/state","OPEN" if s["open"] else "CLOSED")
  elif d=="smart_socket": self.pub("smarthome/smart_socket/state","ON" if s["power"] else "OFF"); self.pub("smarthome/smart_socket/power",s["consumption"])
 def connect(self,c,u,f,rc,*args):
  c.subscribe("smarthome/+/set"); c.subscribe("smarthome/+/+/set")
  for d in self.s: self.device(d)
 def message(self,c,u,m):
  p=m.topic.split("/"); v=m.payload.decode()
  with self.lock:
   if len(p)==3:
    d=p[1]
    if d=="thermostat":
     try:self.s[d]["target_temp"]=float(v)
     except:pass
    elif d in self.s and "power" in self.s[d] and v in ("ON","OFF"): self.s[d]["power"]=(v=="ON")
   elif len(p)==4:
    d=p[1]
    if d in self.s and p[2]=="brightness":
     try:self.s[d]["brightness"]=max(0,min(100,int(float(v))))
     except:pass
   if d in self.s:self.device(d)
 def climate(self):
  while self.running:
   with self.lock:
    s=self.s["thermostat"]; delta=s["target_temp"]-s["current_temp"]; s["heating"]=delta>0.3
    s["current_temp"]+=random.uniform(.1,.25) if delta>.3 else random.uniform(-.15,-.05) if delta<-.3 else random.uniform(-.05,.05); self.device("thermostat")
   time.sleep(10)
 def sensors(self):
  while self.running:
   with self.lock:
    if random.random()<.05:
     self.s["motion_detector"]["motion"]=True; self.device("motion_detector"); threading.Timer(5,self.reset_motion).start()
    if random.random()<.01:self.s["door_sensor"]["open"]=not self.s["door_sensor"]["open"]; self.device("door_sensor")
    so=self.s["smart_socket"]; so["consumption"]=random.randint(50,220) if so["power"] else 0; self.device("smart_socket")
   time.sleep(5)
 def reset_motion(self):
  with self.lock:self.s["motion_detector"]["motion"]=False; self.device("motion_detector")
 def run(self):
  self.c.on_connect=self.connect; self.c.on_message=self.message; self.c.connect("localhost",1883,60); self.c.loop_start()
  threading.Thread(target=self.climate,daemon=True).start(); threading.Thread(target=self.sensors,daemon=True).start()
  print("SmartHome simulator running; Ctrl+C to stop")
  try:
   while True:time.sleep(1)
  except KeyboardInterrupt:self.running=False; self.c.loop_stop(); self.c.disconnect()
if __name__=="__main__":Simulator().run()
