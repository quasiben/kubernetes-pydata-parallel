#!/bin/bash

if [ -z ${GIT_URL+x} ]; then
    echo "GIT_URL is unset";
else
    echo "GIT_URL is set to '$GIT_URL'";
    git clone $GIT_URL /opt/app/
fi

python /tmp/register.py
jupyter notebook --ip='*' --port=8080 --no-browser --notebook-dir /opt/app/ --NotebookApp.base_url=/$APP_ID 1> /tmp/notebook.log 2>&1 &
start-master.sh -h 0.0.0.0 -p 7077 --webui-port 7000
ipcontroller &
dask-scheduler --port=9000 --http-port=9001 --bokeh-port=9002 --bokeh-whitelist="*"
