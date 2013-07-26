import requests
from py2neo import neo4j
import networkx as net
from networkx import algorithms
from pandas import DataFrame


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


def create_nodes(args=list):
    try:
        list_dicts = []
        for prodList in getData():
            if len(prodList[0]) != 0:
                dict_object = dict(zip(args, prodList))
                list_dicts.append(dict_object)
        return list_dicts
    except IndexError:
        raise IndexError
    except KeyError:
        raise KeyError


def clusterData(args, column_name):
    gd = DataFrame(create_nodes(args)).groupby(column_name)
    asn_groups = [x[0] for x in gd]
    for asn in asn_groups:
        df = gd.get_group(asn)
        create_dict = [{k: df.values[i][v] for v, k in enumerate(df.columns)} for i in range(len(df))]
        yield create_dict


def main():
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    args = ["fqdn", "asn", "ipaddr"]
    column_name = 'asn'
    all_nodes = []
    for cluster in clusterData(args, column_name):
        for i, e1 in enumerate(cluster):
            all_nodes.append(e1)
            for j, e2 in enumerate(cluster):
                if e1 != e2:
                    if e1['asn'] != '8560':
                        all_nodes.append((i, "RELATED", j))
    graph_db.create(all_nodes)


if __name__ == '__main__':
    main()