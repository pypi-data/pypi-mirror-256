import time
import telnetlib
import asyncio
import paho.mqtt.client as mqtt
from threading import Thread

from .exceptions import MessageTimeout
from .structs import topicsMQTT
from .config import *


DEBUG = True

class Poll:
    
    def __init__(self):
        pass


    def poll(func, val=None, timeout=None):

        start = time.time()

        res = func()
        while res == val:

            res = func()

            if timeout != None:
                if time.time() - start  > timeout:
                    raise MessageTimeout
                
            time.sleep(0.01)

        return res


class ARCL:

    def __init__(self, ipLD90, portLD90):

        self.ipLD90 = ipLD90
        self.portLD90 = portLD90
        self.timeout = 3

        self.tn = telnetlib.Telnet(self.ipLD90, self.portLD90, timeout=5)
        self.tn.read_until(b"\r\n")

        self.tn.write(b"12345\r\n")

        response = self.tn.read_until(b"\r\n")
        if b"Welcome to the server.\r\n" in response:
            print("Registration success.")
        else:
            raise ConnectionError
        
    
    def send_arcl(self, inp: str):

        w = inp + "\r\n"
        w = bytes(w, "utf-8")
        self.tn.write(w)


    def read_arcl(self, end, func, arg, timeout=3):

        a = -1
        while True:
        
            if self.timeout != None:
                arcl = self.tn.read_until(b"\r\n")
            else:   
                arcl = self.tn.read_until(b"\r\n", timeout=timeout)

            arcl = arcl.decode('ascii')
            #print(arcl)
            
            a = arcl.find(end)
            if a != -1:
                l = len(end)
                return arcl[a + l + 1:]
            
            f = arcl.find("Failed")
            if f != -1 and func != print:
                self.send_arcl("say Sensor blocked")
                time.sleep(5)
                func(arg)
    
    def close(self):
        self.tn.write(b"EXIT\r\n")
        self.tn.close()


class MQTT:
    def __init__(self, broker):

        self.broker = broker

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect

        self.client.connect(self.broker)


    def on_connect(self, client, userdata, flags, rc):
        if DEBUG:
            if rc == 0: print(f"Connected to MQTT Broker: {self.broker}")
            else: print("Failed to connect, return code %d\n", rc)      


    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()


class MQTTReceiver(MQTT):

    def __init__(self, broker, topic):

        super().__init__(broker)
        
        self.topic = topic

        self.client.on_message = self.on_message
        self.client.subscribe(self.topic)
        self.client.loop_start()
        

    def on_message(self, client, userdata, msg):
        self.data = msg.payload.decode("utf-8")


class MQTTReceiverPoll(MQTTReceiver):

    def __init__(self, broker, topic):

        super().__init__(broker, topic)
        self.data = None


    def helper(self):
        if self.data != None:
            data = self.data
            self.data = None
            return data
        

    def receive(self, timeout=None):
        self.msg = Poll.poll(self.helper, None, timeout)
        self.disconnect()
        return {"topic": self.topic, "msg": self.msg}
    

class MQTTWrapperRP:

    def __init__(self, broker, struct):

        self.struct = struct
        self.structC = struct()
        self.typ = self.structC.typ

        self.broker = broker
        self.topics = topicsMQTT(self.struct).topics

        self.timeout = 3
        self.threads = len(self.topics) * [None]
        self.ret = {t: None for t in self.topics}


    def helper(self, topic, timeout):

        mqttRP = MQTTReceiverPoll(self.broker, topic)
        rec = mqttRP.receive(timeout)
        self.ret[rec["topic"]] = self.typ(rec["msg"])


    def start(self):

        for i, t in enumerate(self.topics):
            self.threads[i] = Thread(
                target=self.helper, 
                args=(t, self.timeout))
            self.threads[i].start()
        
        for i in range(len(self.topics)):
            self.threads[i].join()

        self.args = [self.ret[t] for t in self.topics]
        return self.struct(self.args)

    
class MQTTPublisher(MQTT):
        
    def __init__(self, broker):

        super().__init__(broker)


    def publish(self, topic, msg):

        if not isinstance(msg, str):
            msg = str(msg)

        self.client.publish(topic, msg)


class MQTTWrapperPublish:

    def __init__(self, broker, struct):

        self.broker = broker
        self.struct = struct

        self.topics = topicsMQTT(self.struct).topics
    
        l = len(self.topics)
        self.clients =  l * [MQTTPublisher(self.broker)]

    
    def publish(self, structC):

        for i in range(len(self.topics)):

            c = self.clients[i]
            t = self.topics[i]
            msg = structC.ret[i]
            c.publish(t, msg)


class MQTTPassthrough:

    def __init__(self, brokerFrom, brokerTo, topic):

        self.brokerFrom = brokerFrom
        self.brokerTo = brokerTo
        self.topic = topic

        self.rec = MQTT(self.brokerFrom)
        self.rec.client.on_message = self.on_message
        self.rec.client.subscribe(self.topic)

        self.pub = MQTTPublisher(self.brokerTo)

        self.rec.client.loop_forever()
        
        
    def on_message(self, client, userdata, msg):

        self.topic = msg.topic
        self.msg = msg.payload.decode("utf-8")
        if DEBUG:
            print(self.topic)
            print(self.msg)
        self.pub.publish(self.topic, self.msg)