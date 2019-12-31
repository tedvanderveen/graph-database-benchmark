############################################################
# Copyright (c)  2015-now, TigerGraph Inc.
# All rights reserved
# It is provided as it is for benchmark reproducible purpose.
# anyone can use it for benchmark purpose with the
# acknowledgement to TigerGraph.
# Author: Mingxi Wu mingxi.wu@tigergraph.com
############################################################

# from neo4j.v1 import GraphDatabase, basic_auth
import redis
import requests

import config


class QueryRunner():
    def __init__(self):
        pass

    def KN(self, root):
        pass

    def SSSP(self, root):
        pass

    def PG(self):
        pass

    def WCC(self):
        pass

    def LCC(self):
        pass


class RedisGraphQueryRunner(QueryRunner):
    def __init__(self, graphid, label, url="127.0.0.1:6379", connection_pool=None, passwd=None):
        QueryRunner.__init__(self)
        ip, port = url.split(':')
        self.graphid = graphid
        self.label = label
        if connection_pool is None:
            self.connection_pool = redis.ConnectionPool(host=ip, port=port, password=passwd)
        else:
            self.connection_pool = connection_pool
        self.driver = redis.StrictRedis(connection_pool=self.connection_pool)

    def KN(self, root, depth):
        try:
            query = "MATCH (s:%s)-[*%d]->(t) WHERE s.id=%d RETURN count(t)" % (self.label, int(depth), int(root))
            result = self.driver.execute_command('graph.query', self.graphid, query)
        except Exception as e:  # timeout, we return -1, reset session
            print("Query '%s' resulted in Exception: %s" % (query,e))
            raise e
            return -1
        else:
            print(result)
            print(result[1])
            #  [0][0] [0][1]
            # [[b'count(t)'], [[115956]], [b'Query internal execution time: 29.827944 milliseconds']]
            # [[b'count(t)'], [], [b'Query internal execution time: 0.387752 milliseconds']]

            return float(result[1][0][0]) if len(result[1]) > 0 else 0


# TigerGraph query runner (compatible with v2.1.8)
class TigerGraphQueryRunner(QueryRunner):
    def __init__(self, url=config.TIGERGRAPH_HTTP):
        QueryRunner.__init__(self)
        self.session = requests.Session()
        self.url = url

    def KN(self, root, depth):
        result = self.session.get(self.url + "/query/khop", params={'start_node': root, "depth": depth}).json()
        return result["results"][0]["Start.size()"]

    def PG(self, iteration):
        result = self.session.get(self.url + "/query/pagerank",
                                  params={'iteration': iteration, "dampingFactor": 0.8}).json()
        print (result)

    def WCC(self):
        result = self.session.get(self.url + "/query/wcc").json()
        print (result)
