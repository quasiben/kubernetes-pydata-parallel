#!/bin/bash
python /tmp/register.py
dask-scheduler --port=9000 --http-port=9001 --bokeh-port=9002
