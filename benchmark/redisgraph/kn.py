#!/usr/bin/env python

############################################################
# Copyright (c)  2015-now, TigerGraph Inc.
# All rights reserved
# It is provided as it is for benchmark reproducible purpose.
# anyone can use it for benchmark purpose with the
# acknowledgement to TigerGraph.
# Author: Mingxi Wu mingxi.wu@tigergraph.com
############################################################
import argparse
import multiprocessing
import os
import sys
from timeit import default_timer as timer

from query_runner import *

# Global, map of reports.
seedReports = {}


#####################################################################
# Initialize seed reporting,
# seedReports[seed][iterations] contains the number of iterations required for seed
# seedReports[seed][iterationsSummaryRuns] array of iteration matrices
#######################################################################
def InitSeedReports(seeds, iterations):
    global seedReports
    for s in seeds:
        seedReports[s] = []


#####################################################################
# Generate a report summary.
#######################################################################
def FinalizeReport(seedReports, unique_node_file, depth, threads):
    # seed=19284, k=1, runId=0, avgNeighbor=91.0, execTime=0.197093009949
    # AVG Seed iterations.

    output = ''
    avgKNSize = 0
    avgQueryTime = 0
    threadsTotalRuntime = [0] * threads
    runs = 0

    for seed in seedReports:
        report = seedReports[seed]
        for iterationReport in report:
            avgNeighbor = iterationReport['avgN']
            execTime = iterationReport['totalTime']
            threadId = iterationReport['threadId']
            threadsTotalRuntime[threadId] += execTime
            output += "seed=%s, k=%d, avgNeighbor=%d, execTime=%f[ms]\r\n" % (seed, depth, avgNeighbor, execTime)
            output += "**************************************************************\r\n"

            avgKNSize += avgNeighbor
            avgQueryTime += float(execTime)
            runs += 1

    avgKNSize /= runs
    avgQueryTime /= float(runs)

    # We're interested in how much time did it took us to compute a single query on average
    # Our total run time equals max(threadsTotalRuntime), and we've completed running
    # N queries.
    totalRuntime = max(threadsTotalRuntime)

    output += "summary : avgKNSize=%f, avgQueryTime=%f[ms], totalRuntime=%f[ms]\r\n" % (
        avgKNSize, avgQueryTime, totalRuntime)
    output += "**************************************************************\r\n"

    return output


#####################################################################
# K-hop-path-neighbor-count benchmark workload.
# (1) read prepared random nodes from a seed file under seed folder.
#######################################################################
def GetSeeds(seed_file_path, count):
    if not os.path.exists(seed_file_path):
        print("Seed file does not exists: " + seed_file_path)
        sys.exit()

    # Open seed file
    with open(seed_file_path, 'r') as f:
        pre_nodes = f.read().split()
        if len(pre_nodes) >= count:
            return pre_nodes[0:count]
        else:
            print("Seed file does not contain enough seeds.")
            sys.exit()


###############################################################
# function: thread worker, pull work item from pool
# and execute query via runner
################################################################
def RunKNLatencyThread(datadir, graphid, threadId, depth, provider, label, seedPool, reportQueue, iterations, url,
                       seed):
    if provider == "redisgraph":
        runner = RedisGraphQueryRunner(graphid, label, url)
    elif provider == "tigergraph":
        runner = TigerGraphQueryRunner()
    else:
        print("Unknown runner %s, quiting" % provider)
        sys.exit()

    # As long as there's work to do...
    while not seedPool.empty():
        # Try to get a seed from pool
        seed = None
        try:
            seed = seedPool.get(True, 2)
        except Exception as inst:
            break

        # Make sure we've got a seed.
        if not seed:
            # Failed to get seed from pool, pool probably empty
            break

        iterationSummary = {}
        start = timer()
        # the k-hop distinct neighbor size.
        knsize = runner.KN(seed, depth)
        # for timeout query, we return -1
        end = timer()
        if knsize == -1:
            iterationTime = -1
        else:
            iterationTime = end - start
            iterationTime *= 1000  # convert from seconds to ms

        iterationSummary['threadId'] = threadId
        iterationSummary['seed'] = seed
        iterationSummary['avgN'] = knsize
        iterationSummary['totalTime'] = iterationTime
        reportQueue.put(iterationSummary, False)


###############################################################
# function: check the total latency for k-hop-path neighbor count
# query for a given set of seeds.
################################################################


def RunKNLatency(data_dir, graphid, count, depth, provider, label, threads, iterations, url, seed, stdout):
    # create result folder
    global seedReports
    seedfile = os.path.join(data_dir, seed)
    seeds = GetSeeds(seedfile, count)
    print "## Seeds len {}".format(len(seeds))

    # Create a pool of seeds.
    seedPool = multiprocessing.Queue(len(seeds) * iterations)

    # Thread will report their output using this queue.
    reportQueue = multiprocessing.Queue(len(seeds) * iterations)

    # Add each seed to pool.
    for s in seeds:
        for iter in range(iterations):
            seedPool.put(s)

    # Initialize seed reports
    InitSeedReports(seeds, iterations)
    threadsProc = []
    for tid in range(threads):
        p = multiprocessing.Process(target=RunKNLatencyThread,
                                    args=(
                                        data_dir, graphid, tid, depth, provider, label, seedPool, reportQueue,
                                        iterations,
                                        url, seed))
        threadsProc.append(p)

    # Launch threads
    for t in threadsProc:
        t.start()

    # Wait for all threads to join
    for t in threadsProc:
        t.join()

    # Aggregate reports
    print("Aggregate reports")
    while not reportQueue.empty():
        report = reportQueue.get(False)
        seed = report['seed']
        avgN = report['avgN']
        threadId = report['threadId']
        totalTime = report['totalTime']
        seedReports[seed].append({'avgN': avgN, 'totalTime': totalTime, 'threadId': threadId})

    print("Finalizing report")
    unique_node_file = os.path.join(data_dir, label)
    print unique_node_file
    output = FinalizeReport(seedReports, unique_node_file, depth, threads)

    if stdout is False:

        dirName = "./result_" + provider + "/"
        fileName = "KN-latency-k%d-threads%d-iter%d" % (depth, threads, iterations)
        outputPath = os.path.join(dirName, fileName)

        if not os.path.exists(dirName):
            os.makedirs(dirName)

        with open(outputPath, 'wt') as ofile:
            ofile.write(output)

    else:
        print output

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="check the total latency for k-hop-path neighbor count.")
    parser.add_argument(
        "--graphid", "-g", type=str, default='graph500_22', help="graph id"
    )
    parser.add_argument(
        "--count", "-c", type=int, default=1, help="number of seeds"
    )
    parser.add_argument(
        "--depth", "-d", type=int, default=1, help="number of hops to perform"
    )
    parser.add_argument(
        "--provider", "-p", type=str, default="redisgraph", help="graph identifier"
    )
    parser.add_argument(
        "--url", "-u", type=str, default="127.0.0.1:6379", help="DB url"
    )
    parser.add_argument(
        "--label", "-l", type=str, default="graph500_22_unique_node", help="node label"
    )
    parser.add_argument(
        "--seed", "-s", type=str, default="seed", help="seed file"
    )
    parser.add_argument(
        "--data_dir", type=str, default="data", help="data dir"
    )
    parser.add_argument(
        "--threads", "-t", type=int, default=1, help="number of querying threads"
    )
    parser.add_argument(
        "--iterations", "-i", type=int,  default=1, help="number of iterations per query"
    )
    parser.add_argument('--stdout', type=bool, default=True, help="print report to stdout")

    args = parser.parse_args()
    RunKNLatency(args.data_dir, args.graphid, args.count, args.depth, args.provider, args.label, args.threads,
                 args.iterations, args.url, args.seed, args.stdout)
