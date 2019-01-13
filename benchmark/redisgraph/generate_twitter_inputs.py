import os
import sys
import string

# Read the node input file and translate the input IDs into a contiguous range.
# Then, read the relation input file and translate all source and destination node IDs
# to their updated contiguous values.

# User-provided input data directory
if len(sys.argv) < 2 or os.path.exists(sys.argv[1]) == False:
    print("Usage: generate_inputs.py [path_to_inputs]")
    exit(1)

inputdir = sys.argv[1]

# Input filenames
nodefile = 'twitter_rv.net_unique_node'
nodefile_out = 'twitter_rv_net_unique_node'
relfile = 'twitter_rv'

# Output data directory
datadir = 'data'

# Create updated data directory if it doesn't exist
try:
    os.mkdir(datadir)
except OSError:
    pass

# Count the number of unique nodes in the data set
num_nodes = sum(1 for line in open(os.path.join(inputdir, nodefile)))

updated_id = 0

updated_node_file = open(os.path.join(datadir, nodefile_out), 'w')
updated_node_file.write('id\n') # Output a header row
updated_relation_file = open(os.path.join(datadir, relfile), 'w')

# Scan the node file to find the highest node ID
max_node = -1
with open(os.path.join(inputdir, nodefile)) as f:
    for line in f:
        max_node = max(max_node, int(line))

# Map every node ID to its line number
# and generate an updated node file.
placement = [0]*(max_node + 1)
with open(os.path.join(inputdir, nodefile)) as f:
    for line in f:
        node = int(line)
        placement[node] = updated_id
        updated_id += 1
        updated_node_file.write('%d\n' % (updated_id))

with open(os.path.join(inputdir, relfile)) as f:
    for line in f:
        # Tokenize every line and convert the data to ints
        src, dst = map(int, line.split())

        # Retrieve the updated ID of each source and destination
        a = placement[src]
        b = placement[dst]

        # Output the updated edge description
        updated_relation_file.write("%d,%d\n" % (a, b))

updated_node_file.close()
updated_relation_file.close()
