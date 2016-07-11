#!/bin/bash
git clone https://github.com/dask/distributed.git
pushd distributed
python setup.py install
popd
