if [ ! -d "$1" ] || [ ! -d "$2" ]; then
  echo "Usage: ./redisgraph_load_twitter.sh path/to/redisgraph/ path/to/inputs"
  exit 1
fi

# Prepare input files in RedisGraph bulk import format
python generate_twitter_inputs.py $2 || exit 1

# Run RedisGraph bulk import script
python $1/demo/bulk_insert/bulk_insert.py twitter_rv -n data/twitter_rv_net_unique_node -r data/twitter_rv || exit 1

# Create index on node ID property
~/redis/src/redis-cli GRAPH.QUERY twitter_rv "create index on :twitter_rv_net_unique_node(id)"
