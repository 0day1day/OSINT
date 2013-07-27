from py2neo import neo4j


from py2neo import neo4j, cypher
graphdb = neo4j.GraphDatabaseService()
topic_index = graphdb.get_or_create_index(neo4j.Node, "node_index")
batch = neo4j.WriteBatch(graphdb)
batch.get_or_create_indexed_node('node_index', 'name', 'Alice', {'name': 'Alice'})
batch.get_or_create_indexed_node('node_index', 'name', 'Bob', {'name': 'Bob'})
batch.get_or_create_indexed_relationship('rel_index', 'type', 'KNOWS', 0, 'KNOWS', 1, {})
results = batch.submit()