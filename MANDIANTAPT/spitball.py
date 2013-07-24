import requests
from py2neo import neo4j

"""
Example Single Batch Processed

Batch process creation 3 nodes - where all 3 nodes are related

tuple of 3 nodes: ({'fqdn': 'advanbusiness.com'}, {'asn': '33626'}, {'ipaddr': '208.73.211.165'})

Original Manadiant APT1 released of indicator

advanbusiness.com,33626,208.73.211.165,US,United States,CA,California,Los Angeles,34.0533,-118.2549,803,213,America/Los_Angeles,NA,90071,Oversee.net,Oversee.net,domainservice.com,AS33626 Oversee.net,Corporate,business,534,99,20,60,10

Relationships: Bi-directional - in_relationship & out_relationship

Complete processed data set results in:

Nodes: 5001
Properties: 5001
Relationships: 10002
"""


def getData():
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def create_nodes(*args):
    try:
        list_dicts = []
        for prodList in getData():
            if len(prodList[0]) != 0:
                dict_object = dict(zip([args], [prodList]))
                # dict_object1 = dict(zip([args[0]], [prodList[0]]))
                # dict_object2 = dict(zip([args[1]], [prodList[1]]))
                # dict_object3 = dict(zip([args[2]], [prodList[2]]))
                # dict_object1.update(dict_object2)
                # dict_object1.update(dict_object3)
                # list_dicts.append(dict_object1)
                list_dicts.append(dict_object)
        for nodeObj in list_dicts:
            yield nodeObj
    except IndexError:
        raise IndexError
    except KeyError:
        raise KeyError


def main():
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    args = ["fqdn", "asn", "ipaddr"]
    for nodes in create_nodes(*args):
        print nodes
        # graph_db.create(
        #     nodes[0], nodes[1], nodes[2],
        #     (0, "RELATED", 1),
        #     (0, "RELATED", 2),
        #     (1, "RELATED", 0),
        #     (1, "RELATED", 2),
        #     (2, "RELATED", 0),
        #     (2, "RELATED", 1),
        # )


if __name__ == '__main__':
    main()