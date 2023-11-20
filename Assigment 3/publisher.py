import paho.mqtt.client as mqtt
import time
import datetime
import numpy as np

def on_message(client, userdata, message):
    print(f"\nmessage payload: {message.payload.decode('utf-8')}")
    print(f"message topic: {message.topic}")
    print(f"message qos: {message.qos}")
    print(f"message retain flag: {message.retain}")


class Client:
    def __init__(self, id, on_message):
      self.client = mqtt.Client(id)
      self.ID = id
      self.client.on_message = on_message
    
    def connect(self, broker_address):
      try:
        self.client.connect(broker_address) # connect to broker
        self.client.loop_start()
        print(f"Connected to {broker_address}.")
      except Exception as e:
         print(f"Error: {e}")
    
    def subscribe(self, topic):
      try:
        self.client.subscribe(topic) # subscribe
        print(f"Subscribed to {topic}.")
      except Exception as e:
         print(f"Error: {e}")
          
    def publish(self, topic, message=None, qos=None):
      try:
        if message is not None:
          self.client.publish(topic, message, qos=qos) # publish # subscribe
          print(f"Published {message} to {topic}.")
      except Exception as e:
        print(f"Error: {e}")

    def unsubscribe(self, topic):
      try:
         self.client.unsubscribe(topic)
         print(f"Unsubscribed to {topic}.")
      except Exception as e:
         print(f"Error: {e}")

    def disconnect(self):
      try:
        self.client.loop_stop()  # stop the event processing loop
        self.client.disconnect()
        print("Client Disconnected.")
      except Exception as e:
         print(f"Error: {e}")

broker_address = "test.mosquitto.org"
topic = "teds22/group04/pressure"

client = Client("P1", on_message)
client.connect(broker_address)
client.subscribe(topic)

mu, sigma = 1200.00, 1.0

for i in range(10):
  reading = f'{round(np.random.normal(mu, sigma), 2):.2f}'        
  dt = datetime.datetime.now()
  dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
  message = f'{reading}|{dt}'
  client.publish(topic, message=message, qos=2)
  time.sleep(1)

time.sleep(4)
client.unsubscribe(topic)
client.disconnect()