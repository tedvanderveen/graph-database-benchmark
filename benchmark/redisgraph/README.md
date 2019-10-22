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

This article documents the details on how to reproduce the graph database benchmark result on RedisGraph.

 Data Sets
===========
- graph500 edge file: http://service.tigergraph.com/download/benchmark/dataset/graph500-22/graph500-22
- graph500 vertex file: http://service.tigergraph.com/download/benchmark/dataset/graph500-22/graph500-22_unique_node

- twitter edge file: http://service.tigergraph.com/download/benchmark/dataset/twitter/twitter_rv.tar.gz
- twitter vertex file: http://service.tigergraph.com/download/benchmark/dataset/twitter/twitter_rv.net_unique_node

Hardware & Major environment
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

------------------------------------

# Setup the benchmark
```bash
git clone https://github.com/filipecosta90/graph-database-benchmark.git
cd graph-database-benchmark/benchmark/redisgraph
sudo pip install -r requirements.txt
```

Loading data
==============
```bash
nohup ./redisgraph_load_graph500.sh
nohup ./redisgraph_load_twitter.sh
```


Run K-hop neighborhood count benchmark
================
Change graph500-22-seed and twitter_rv.net-seed path to your seed file path.

Results will be stored in "result_redisgraph" output directory.

Graph500
-----------------

```bash
# 300 seeds, depth 1
nohup python kn.py -g graph500 -s graph500-22-seed -c 300 -d 6 -p redisgraph -l graph500-22_unique_node -t 22 -i 1
# 300 seeds, depth 2
nohup python kn.py -g graph500 -s graph500-22-seed -c 300 -d 6 -p redisgraph -l graph500-22_unique_node -t 22 -i 2
# 10 seeds, depth 3
nohup python kn.py -g graph500 -s graph500-22-seed -c 10 -d 6 -p redisgraph -l graph500-22_unique_node -t 22 -i 3
# 10 seeds, depth 6
nohup python kn.py -g graph500 -s graph500-22-seed -c 10 -d 6 -p redisgraph -l graph500-22_unique_node -t 22 -i 6
```


Twitter Benchmark
-------------

```bash
# 300 seeds, depth 1
nohup python kn.py -g twitter_rv -s twitter_rv_net-seed -c 300 -d 6 -p redisgraph -l twitter_rv_net_unique_node -t 22 -i 1
# 300 seeds, depth 2
nohup python kn.py -g twitter_rv -s twitter_rv_net-seed -c 300 -d 6 -p redisgraph -l twitter_rv_net_unique_node -t 22 -i 2
# 10 seeds, depth 3
nohup python kn.py -g twitter_rv -s twitter_rv_net-seed -c 10 -d 6 -p redisgraph -l twitter_rv_net_unique_node -t 22 -i 3
# 10 seeds, depth 6
nohup python kn.py -g twitter_rv -s twitter_rv_net-seed -c 10 -d 6 -p redisgraph -l twitter_rv_net_unique_node -t 22 -i 6
```