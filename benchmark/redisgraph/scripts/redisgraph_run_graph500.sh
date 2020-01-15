#!/usr/bin/env bash

DATASET_DIR=${DATASET_DIR:-"graph500_22"}
ITERATIONS_PER_QUERY=${ITERATIONS_PER_QUERY:-10}
SEEDS=${SEEDS:-10}

EXE_DIR=${EXE_DIR:-$(dirname $0)}
source ${EXE_DIR}/common.sh

NODE_FILENAME=${NODE_FILENAME:-"graph500_22_unique_node_out"}

DATA_NODE_FILE_NAME=${DATASET}/graph500_22_out_noheader


# How many queries would be run
SLEEP_BETWEEN_RUNS=${SLEEP_BETWEEN_RUNS:-"60"}

for DEPTH in 1 2 3 6; do
for WORKERS in 1 22; do
for run in 1 2 3; do
    echo "Running depth ${DEPTH}. Workers ${WORKERS}. RUN $run"

    python3 kn.py --url ${DATABASE_HOST}:${DATABASE_PORT} -g graph500_22 -s ${DATA_NODE_FILE_NAME} \
    -c ${SEEDS} -d ${DEPTH} -p redisgraph -l ${NODE_FILENAME} \
    --threads ${WORKERS} -i ${ITERATIONS_PER_QUERY} --stdout > ${PREFIX}_${WORKERS}_workers_${DEPTH}_depth_run_${run}

    echo "Sleeping for ${SLEEP_BETWEEN_RUNS} seconds"
    sleep ${SLEEP_BETWEEN_RUNS}
done
done
done

