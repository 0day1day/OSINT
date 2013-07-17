__date__ = "July 14, 2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Laboratory"


import requests
from bulbs.neo4jserver import Graph
from bulbs.neo4jserver import Graph.


def getData():
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def main():
    g = Graph()
    g.edges.create(7, "related", 8)
    try:
        g = Graph()
        keys = ["fqdn", "asn", "ipaddress"]
        for prodList in getData():
            if len(prodList[0]) != 0:
                values = [prodList[0], prodList[1], prodList[2]]
                dict_object = dict(zip(keys, values))
                g = Graph()
                g.vertices.create(dict_object)
    except IndexError:
        raise IndexError


if __name__ == '__main__':
    main()