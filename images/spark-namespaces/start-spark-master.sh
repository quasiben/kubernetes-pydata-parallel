#!/bin/bash
python /tmp/register.py

start-master.sh -h 0.0.0.0 -p 7077 --webui-port 7000

tail -f /opt/conda/share/spark/logs/spark--org.apache.spark.deploy.master.Master*
