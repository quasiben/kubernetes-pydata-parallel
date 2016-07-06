#!/bin/bash
python /tmp/register.py

start-master.sh -h 0.0.0.0 -p 7077 --webui-port 7000
start-slave.sh spark://localhost:7077

tail -f /opt/conda/share/spark/logs/spark--org.apache.spark.deploy.worker.Worker*
