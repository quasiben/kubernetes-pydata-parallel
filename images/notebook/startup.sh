#!/bin/bash
jupyter notebook --ip='*' --port=8080 --no-browser --notebook-dir /opt/app/ --NotebookApp.base_url=/$APP_ID
