#!/usr/bin/env bash

DATASET_DIR=${DATASET_DIR:-"graph500_22"}
ITERATIONS_PER_QUERY=${ITERATIONS_PER_QUERY:-10}
SEEDS=${SEEDS:-10}
DEPTH=${DEPTH:-1}

# How many concurrent worker would run queries - match num of cores, or default to 8
WORKERS=${WORKERS:-$(grep -c ^processor /proc/cpuinfo 2>/dev/null || echo 8)}

EXE_DIR=${EXE_DIR:-$(dirname $0)}
source ${EXE_DIR}/common.sh

DATA_NODE_FILE_NAME=${DATASET}/graph500_22_unique_node

# 300 seeds, depth 1
python3 kn.py --url ${DATABASE_HOST}:${DATABASE_PORT} --password ${PASSWORD} -g graph500_22 -s ${DATA_NODE_FILE_NAME} -c ${SEEDS} -d ${DEPTH} -p redisgraph -l graph500_22_unique_node -t ${WORKERS} -i ${ITERATIONS_PER_QUERY} --stdout || exit 1
