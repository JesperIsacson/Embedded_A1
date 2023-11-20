from rdflib import Graph

graph = Graph()

graph.parse("./pressure.ttl")

query = """
PREFIX sosa: <http://www.w3.org/ns/sosa/>

SELECT ?timeStamp ?pressure
WHERE {
    ?obs a sosa:Observation ;
         sosa:hasSimpleResult ?timeStamp ;
         sosa:resultTime ?pressure .
}
ORDER BY (?timeStamp)
"""

output = graph.query(query)

for row in output:
    print(f"{row.timeStamp} | {row.pressure}")
