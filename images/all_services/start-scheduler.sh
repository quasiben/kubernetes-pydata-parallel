#!/bin/bash

if [ -z ${PARALLEL_GIT_URL+x} ]; then
    echo "PARALLEL_GIT_URL is unset";
else
    echo "PARALLEL_GIT_URL is set to '$PARALLEL_GIT_URL'";
    cd /opt/app/parallel-tutorial && git pull
fi

if [ -z ${DASK_GIT_URL+x} ]; then
    echo "DASK_GIT_URL is unset";
else
    echo "DASK_GIT_URL is set to 'DASK_GIT_URL'";
    cd /opt/app/dask-tutorial && git pull origin scipy-2017
fi


python /tmp/register.py
jupyter notebook --ip='*' --port=8080 --no-browser --notebook-dir /opt/app/ --NotebookApp.base_url=/$APP_ID --NotebookApp.password="sha1:cada2db614c6:420481e8169fc3317c2115b952344ea6bd8162a0" 1> /tmp/notebook.log 2>&1 &
/opt/conda/sbin/start-master.sh -h 0.0.0.0 -p 7077 --webui-port 7000 
ipcontroller &
dask-scheduler --port=9000 --bokeh-port=9002 --bokeh-whitelist="*" --bokeh-prefix=/${APP_ID}/9002 --use-xheaders=True
