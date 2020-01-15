#!/usr/bin/env bash

# How many queries would be run
HOST=${MAX_QUERIES:-"localhost"}

# How many queries would be run
SLEEP_BETWEEN_RUNS=${SLEEP_BETWEEN_RUNS:-"60"}

for depth in 1 2 3 6; do
for worker_num in 1 22; do
    echo "Running depth ${depth}. Workers ${worker_num}"

    #WORKERS=${worker_num} DATABASE_HOST=${HOST} BULK_DATA_DIR=/root/bulk_data DEPTH=${depth} SEEDS=100000 ITERATIONS_PER_QUERY=10 ./scripts/redisgraph_run_graph500.sh

    echo "Sleeping for ${SLEEP_BETWEEN_RUNS} seconds"
    sleep ${SLEEP_BETWEEN_RUNS}
done
done

