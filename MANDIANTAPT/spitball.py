import requests
from py2neo import neo4j, node, rel




def getData():
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def main():
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    try:
        key1 = ["fqdn"]
        key2 = ["asn"]
        key3 = ["ipaddr"]
        for prodList in getData():
            if len(prodList[0]) != 0:
                dict_object1 = dict(zip(key1, [prodList[0]]))
                dict_object2 = dict(zip(key2, [prodList[1]]))
                dict_object3 = dict(zip(key3, [prodList[2]]))
                print(dict_object1, dict_object2, dict_object3)
    except IndexError:
        raise IndexError


if __name__ == '__main__':
    main()