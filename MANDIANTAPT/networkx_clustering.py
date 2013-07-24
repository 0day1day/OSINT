import requests
import networkx as net
from itertools import chain


def getData():
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def degreeCentrality(graph_name):
    """Degree Centrality - Most Frequent or Most Popular"""
    deg = net.degree(graph_name)
    ms = sorted(deg.iteritems(), key=lambda (k,v): (-v,k))
    return ms


def main():
    try:
        node_list = []
        for node in getData():
            fqdn = node[0]
            asn = node[1]
            nodes = (fqdn, asn)
            node_list.append(nodes)
        #flatten_list = list(chain(node_list))
        print node_list
    except IndexError:
        pass
    #     g = net.Graph(flatten_list)
    # #     # Identify Frequency an ASN is utilized - identifying patterns in routes of movement by APT actors - which ASN's did they utilize most
    # print "Top ASN Routes Utilized By Mandiant Identified APT Actors"
    # print "===="
    # for item in degreeCentrality(g):
    #     if item[1] > 3:
    #         print item
    # print "===="
    # print "\n"

if __name__ == '__main__':
    main()
