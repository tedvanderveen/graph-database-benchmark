Graph Database Benchmark : 




# Full-Text Search Benchmark (FTSB)
This repo contains code for benchmarking Graph databases.

- same datasets
- same query workload
- same enviroment (hardware)
- cross validation of result
- each vendor's benchmark is under
 /benchmark/vendor_name/
- start with README under each folder
- all test can be reproducible on EC2 or similar enviroment.

Contact: benchmark@tigergraph.com

Current databases supported:

+ Amazon Neptune [(benchmark folder)](benchmark/neptune/)
+ Arangodb  [(benchmark folder)](benchmark/arangodb/)
+ JanusGraph [(benchmark folder)](benchmark/janusgraph/)
+ Neo4j [(benchmark folder)](benchmark/neo4j/)
+ RedisGraph [(benchmark folder)](benchmark/redisgraph/)
+ TigerGraph [(benchmark folder)](benchmark/tigergraph/)

