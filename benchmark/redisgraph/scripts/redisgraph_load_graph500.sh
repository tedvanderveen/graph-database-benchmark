#!/usr/bin/env bash

DATASET_DIR=${DATASET_DIR:-"graph500_22"}

EXE_DIR=${EXE_DIR:-$(dirname $0)}
source ${EXE_DIR}/common.sh

MAX_TOKEN_SIZE=${MAX_TOKEN_SIZE:-8}
NODE_FILENAME=${NODE_FILENAME:-"graph500_22_unique_node_out"}

redis-cli -h ${DATABASE_HOST} -p ${DATABASE_PORT} del ${KEYNAME} 

# Run RedisGraph bulk import script
python3  bulk_insert.py ${KEYNAME} --max-token-size ${MAX_TOKEN_SIZE} -n ${DATASET}/${NODE_FILENAME} -r ${DATASET}/graph500_22_out \
  --host ${DATABASE_HOST} --port ${DATABASE_PORT} || exit 1

# Create index on node ID property
redis-cli -h ${DATABASE_HOST} -p ${DATABASE_PORT} graph.query ${KEYNAME} "create index on :${NODE_FILENAME}(id)"