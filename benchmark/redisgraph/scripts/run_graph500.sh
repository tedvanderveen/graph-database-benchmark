#!/usr/bin/env bash

# How many queries would be run
HOST=${MAX_QUERIES:-"localhost"}
PREFIX=${PREFIX:-"master"}
S=${S:-"100000"}
I=${I:-"10"}

# How many queries would be run
SLEEP_BETWEEN_RUNS=${SLEEP_BETWEEN_RUNS:-"60"}

for depth in 1 2 3 6; do
for worker_num in 1 22; do
for run in 1 2 3; do
    echo "Running depth ${depth}. Workers ${worker_num}. RUN $run"

    WORKERS=${worker_num} DATABASE_HOST=${HOST} \
    BULK_DATA_DIR=/root/bulk_data DEPTH=${depth} SEEDS=$S \
    ITERATIONS_PER_QUERY=$I ./scripts/redisgraph_run_graph500.sh > ${PREFIX}_${worker_num}_workers_${depth}_depth_run_${run}

    echo "Sleeping for ${SLEEP_BETWEEN_RUNS} seconds"
    sleep ${SLEEP_BETWEEN_RUNS}
done
done
done

