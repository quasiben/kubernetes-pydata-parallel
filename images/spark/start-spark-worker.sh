#!/bin/bash
start-slave.sh spark://localhost:7077

tail -f /opt/conda/share/spark/logs/spark--org.apache.spark.deploy.worker.Worker*
