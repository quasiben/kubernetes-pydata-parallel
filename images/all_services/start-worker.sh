#!/bin/bash
/opt/conda/sbin/start-slave.sh spark://schedulers:7077
/opt/conda/bin/dask-worker schedulers:9000 --nprocs 1 --nthreads 4 --memory-limit 6e9
