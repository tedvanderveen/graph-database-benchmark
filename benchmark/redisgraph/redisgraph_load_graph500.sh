if [ ! -d "$1" ] || [ ! -d "$2" ]; then
  echo "Usage: ./redisgraph_load_graph500.sh path/to/redisgraph/ path/to/inputs"
  exit 1
fi

# Prepare input files in RedisGraph bulk import format
python generate_graph500_inputs.py $2 || exit 1

# Run RedisGraph bulk import script
python $1/demo/bulk_insert/bulk_insert.py graph500-22 -n data/graph500-22_unique_node -r data/graph500-22 || exit 1

# Create index on node ID property
~/redis/src/redis-cli GRAPH.QUERY graph500-22 "create index on :graph500-22_unique_node(id)"
