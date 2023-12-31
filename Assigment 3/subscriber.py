from publisher import Client
import queue
import functools
import time

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, RDFS, SOSA

def on_message(Que, client, userdata, message):
    print("Message recived")
    Que.put(message.payload.decode('utf-8'))

if __name__=="__main__":
  EX = Namespace('http://example.org')
  earthAtmosphere = EX["earthAtmosphere"]
  iphone7 =  EX["iphone7"]
  sensor_BMP282 =  EX["sensor_BMP282"]
  sensor_BMP282_atmosphericPressure =  EX["sensor_BMP282_atmosphericPressure"]

  g = Graph()

  g.bind('ex', EX)
  g.bind('rdf', RDF)
  g.bind('rdfs', RDFS)
  g.bind('sosa', SOSA)

  g.add( (earthAtmosphere, RDF.type, SOSA.FeatureOfInterest) )
  g.add( (earthAtmosphere, RDFS.label, Literal("Atmosphere of Earth", lang="en")) )

  g.add((iphone7, RDF.type, SOSA.Platform))
  g.add((iphone7, RDFS.label, Literal("IPhone 7 - IMEI 35-207306-844818-0", lang="en")))
  g.add((iphone7, RDFS.comment, Literal("IPhone 7 - IMEI 35-207306-844818-0 - John Doe", lang="en")))
  g.add((iphone7, SOSA.hosts, sensor_BMP282))

  g.add((sensor_BMP282, RDF.type, SOSA.Sensor))
  g.add((sensor_BMP282, RDFS.label, Literal("Bosch Sensortec BMP282", lang="en")))
  g.add((sensor_BMP282, SOSA.observes, sensor_BMP282_atmosphericPressure))

  broker_address = "test.mosquitto.org"
  #broker_address = "localhost"
  topic = "teds22/group04/pressure"
  q = queue.Queue()
  client = Client("Sub", on_message=functools.partial(on_message, q))
  client.connect(broker_address)
  client.loop("simple")
  client.subscribe(topic)

  recived_messages = []
  while(len(recived_messages) < 10):
    if not q.empty(): 
      msg = q.get()
      recived_messages.append(msg)
    time.sleep(0.5)

  client.unsubscribe(topic)
  client.disconnect()

  # Can also be done in on_message but felt cleaner to do here
  for i, msg in enumerate(recived_messages):
    [reading, dt] = msg.split('|')
    Observation =  EX[f"Observation{i}"]

    g.add((Observation, RDF.type, SOSA.Observation))
    g.add((Observation, SOSA.ObservableProperty, sensor_BMP282_atmosphericPressure))
    g.add((Observation, SOSA.hasFeatureOfInterest, earthAtmosphere))
    g.add((Observation, SOSA.madeBySensor, sensor_BMP282))
    g.add((Observation, SOSA.hasSimpleResult, Literal(reading)))
    g.add((Observation, SOSA.resultTime, Literal(dt)))

  with open('./Assigment 3/pressure.ttl', 'w') as f:
    f.write(g.serialize(format="turtle"))