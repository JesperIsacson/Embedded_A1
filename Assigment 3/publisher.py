import paho.mqtt.client as mqtt
import time
import datetime
import numpy as np

class Client:
    def __init__(self, id, on_message=None):
      self.client = mqtt.Client(id)
      self.ID = id
      if on_message is not None:
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


if __name__ == "__main__":
  broker_address = "test.mosquitto.org"
  #broker_address = "localhost"
  topic = "teds22/group04/pressure"

  client = Client("Pub")
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