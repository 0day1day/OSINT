import requests
from py2neo import neo4j
from pandas import DataFrame


def getData():
    """Get CSV Mandiant Data Set - output list data structure"""
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def create_nodes(args=list):
    """Create list of dicts - each dict will represent a node"""
    list_dicts = []
    for prodList in getData():
        if len(prodList[0]) != 0:
            dict_object = dict(zip(args, prodList))
            list_dicts.append(dict_object)
    return list_dicts


def clusterData(args, column_name):
    """Leverage Panadas Groupby to cluster nodes by ASN - Then convert resulting DataFrames in list dicts by cluster"""
    gd = DataFrame(create_nodes(args)).groupby(column_name)
    asn_groups = [x[0] for x in gd]
    for asn in asn_groups:
        df = gd.get_group(asn)
        create_dict = [{k: df.values[i][v] for v, k in enumerate(df.columns)} for i in range(len(df))]
        yield create_dict


def main():
    """Batch create nodes and node relationships in Neo4j"""
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    args = ["fqdn", "asn", "ipaddr"]
    column_name = 'asn'
    all_nodes = []
    for cluster in clusterData(args, column_name):
        for i, e1 in enumerate(cluster):
            all_nodes.append(e1)
            for j, e2 in enumerate(cluster):
                if e1 != e2:
                    all_nodes.append((i, "RELATED", j))
    graph_db.create(*all_nodes)


if __name__ == '__main__':
    main()