#!/bin/bash
start-slave.sh spark://schedulers:7077
ipcluster engines -n 2 &
dask-worker schedulers:9000 --nprocs 2 --nthreads 1
