import requests
from py2neo import neo4j
from py2neo import node
from py2neo import rel
from py2neo import cypher


def getData():
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def create_graph():
    pass


def create_node_properties():
    pass


def create_nodes():
    pass


def create_relationship_properties():
    pass


def create_relationships():
    pass


def generate_node_properties():
    pass


def generate_rel_properties():
    pass


def generate_nodes():
    pass


def generate_rels():
    pass


def create_nodes_index():
    pass


def create_relationships_index():
    pass


def main():
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    try:
        keys = ["fqdn", "asn", "ipaddr"]
        for prodList in getData():
            if len(prodList[0]) != 0:
                dict_object1 = dict(zip(keys[0], [prodList[0]]))
                dict_object2 = dict(zip(keys[1], [prodList[1]]))
                dict_object3 = dict(zip(keys[2], [prodList[2]]))
                print(dict_object1, dict_object2, dict_object3)
    except IndexError:
        raise IndexError


if __name__ == '__main__':
    main()