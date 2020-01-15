#!/usr/bin/env bash

DATASET_DIR=${DATASET_DIR:-"graph500_22"}

EXE_DIR=${EXE_DIR:-$(dirname $0)}
source ${EXE_DIR}/common.sh

redis-cli -h ${DATABASE_HOST} -p ${DATABASE_PORT} del "graph500_22" 

# Run RedisGraph bulk import script
python3  bulk_insert.py graph500_22 -n ${DATASET}/graph500_22_unique_node_out -r ${DATASET}/graph500_22_out \
  --host ${DATABASE_HOST} --port ${DATABASE_PORT} || exit 1

# Create index on node ID property
redis-cli -h ${DATABASE_HOST} -p ${DATABASE_PORT} graph.query "graph500_22" "create index on :graph500_22_unique_node(id)"