from publisher import Client
import queue
import functools
import time
from rdflib.namespace import RDF, RDFS, XSD, SOSA, TIME


def on_message(Que,client, userdata, message):
    print(f"\nmessage payload: {message.payload.decode('utf-8')}")
    Que.put(message.payload.decode('utf-8'))



if __name__=="__main__":
  broker_address = "test.mosquitto.org"
  #broker_address = "localhost"
  topic = "teds22/group04/pressure"
  q = queue.Queue()
  client = Client("Sub", on_message=functools.partial(on_message, q))
  client.connect(broker_address)
  client.subscribe(topic)

  recived_messages = []
  while(len(recived_messages) < 10):
    if not q.empty(): 
      msg = q.get()
      recived_messages.append(msg)
    time.sleep(0.5)
  client.unsubscribe(topic)
  client.disconnect()

  with open('data.txt', 'w') as f:
    for msg in recived_messages:
      f.write(msg + "\n")
      