```bash
############################################################
# Copyright (c)  2015-now, TigerGraph Inc.
# All rights reserved
# It is provided as it is for benchmark reproducible purpose.
# anyone can use it for benchmark purpose with the
# acknowledgement to TigerGraph.
# Author: Mingxi Wu mingxi.wu@tigergraph.com
############################################################
```

Hardware & Major environment requirements
================================
- Amazon EC2 machine r4.8xlarge
- OS Ubuntu 18.04.1 LTS
- Install the required Python modules with the following commands
- 32 vCPUs
- 244 GiB memory
- attached a 250G  EBS-optimized Provisioned IOPS SSD (IO1), IOPS we set is 50 IOPS/GiB

```bash
sudo apt-get update
sudo apt-get install build-essential cmake python-pip python-dev 
sudo pip install --upgrade pip
```

## Current use cases
This article documents the details on how to reproduce the graph database benchmark result on RedisGraph.
Currently, RedisGraph benchmark supports two use cases:


Name | Description and Source | Vertices | Edges
-- | -- | -- | --
graph500 | Synthetic Kronecker graphhttp://graph500.org | 2.4 M | 64 M
twitter | Twitter user-follower directed graphhttp://an.kaist.ac.kr/traces/WWW2010.html | 41.6 M | 1.47 B                                                                                                                                                                                                 

### How to use the benchmark

Graph benchmarking involves 3 phases: data retrieval, data loading/insertion, and query execution.

## Installation
The easiest way to get and install the benchmark code is to use:
```bash
git clone https://github.com/filipecosta90/graph-database-benchmark.git
cd graph-database-benchmark/benchmark/redisgraph
sudo pip install -r requirements.txt
```

#### Data retrieval 

Variables:
1. `DATABASE_HOST` (default: `127.0.0.1`)
1. `DATABASE_PORT` (default: `6379`)
1. `BULK_DATA_DIR` (default: `/tmp/bulk_data`)
1. `DATASET_NAME` (default: `dependent on the use case`)
1. `EDGE_FILE` (default: `dependent on the use case`)
1. `NODE_FILE` (default: `dependent on the use case`)

The easiest way to get the datasets required for the benchmark is to use one of the helper scrips:
1. `get_graph500_dataset.sh`
or
1. `get_twitter_dataset.sh`

Sample output:
```bash
./get_graph500_dataset.sh
```

### Data insertion

##### Graph500
```bash
./redisgraph_load_graph500.sh
```

Sample output:
```bash

```

##### Twitter Benchmark
```bash
./redisgraph_load_twitter.sh
```

Sample output:
```bash

```


### Benchmarking query execution performance

#### Run K-hop neighborhood count benchmark
Change graph500-22-seed and twitter_rv.net-seed path to your seed file path.
Results will be stored in "result_redisgraph" output directory.

##### Graph500

```bash
# 300 seeds, depth 1, 3 iterations per query
nohup python kn.py -g graph500 -s graph500_22_seed -c 300 -d 1 -p redisgraph -l graph500_22_unique_node -t 22 -i 3
# 300 seeds, depth 2, 3 iterations per query
nohup python kn.py -g graph500 -s graph500_22_seed -c 300 -d 2 -p redisgraph -l graph500_22_unique_node -t 22 -i 3
# 10 seeds, depth 3, 3 iterations per query
nohup python kn.py -g graph500 -s graph500_22_seed -c 10 -d 3 -p redisgraph -l graph500_22_unique_node -t 22 -i 3
# 10 seeds, depth 6, 3 iterations per query
nohup python kn.py -g graph500 -s graph500_22_seed -c 10 -d 6 -p redisgraph -l graph500_22_unique_node -t 22 -i 3
```


##### Twitter Benchmark

```bash
# 300 seeds, depth 1, 3 iterations per query
nohup python kn.py -g twitter_rv -s twitter_rv_net_seed -c 300 -d 1 -p redisgraph -l twitter_rv_net_unique_node -t 22 -i 3
# 300 seeds, depth 2, 3 iterations per query
nohup python kn.py -g twitter_rv -s twitter_rv_net_seed -c 300 -d 2 -p redisgraph -l twitter_rv_net_unique_node -t 22 -i 3
# 10 seeds, depth 3, 3 iterations per query
nohup python kn.py -g twitter_rv -s twitter_rv_net_seed -c 10 -d 3 -p redisgraph -l twitter_rv_net_unique_node -t 22 -i 3
# 10 seeds, depth 6, 3 iterations per query
nohup python kn.py -g twitter_rv -s twitter_rv_net_seed -c 10 -d 6 -p redisgraph -l twitter_rv_net_unique_node -t 22 -i 3
```
