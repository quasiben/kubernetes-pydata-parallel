#!/bin/bash
start-slave.sh spark://schedulers:7077
ipcluster engines &
dask-worker schedulers:9000
