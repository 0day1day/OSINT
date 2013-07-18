import requests
import uuid
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


def create_nodes():
    try:
        keys = ["fqdn", "asn", "ipaddr"]
        list_dicts = []
        for prodList in getData():
            if len(prodList[0]) != 0:
                dict_object1 = dict(zip([keys[0]], [prodList[0]]))
                dict_object2 = dict(zip([keys[1]], [prodList[1]]))
                dict_object3 = dict(zip([keys[2]], [prodList[2]]))
                tuple_dicts = (dict_object1, dict_object2, dict_object3)
                list_dicts.append(tuple_dicts)
        for nodeObj in list_dicts:
            yield nodeObj
    except IndexError:
        raise IndexError
    except KeyError:
        raise KeyError


def main():
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    for nodes in create_nodes():
        # key_val1 = uuid.uuid4()
        # key_val2 = uuid.uuid4()
        # key_val3 = uuid.uuid4()
        graph_db.create(
            nodes[0], nodes[1], nodes[2],
            (0, "RELATED", 1),
            (0, "RELATED", 2),
            (1, "RELATED", 0),
            (1, "RELATED", 2),
            (2, "RELATED", 0),
            (2, "RELATED", 1),
        )


if __name__ == '__main__':
    main()