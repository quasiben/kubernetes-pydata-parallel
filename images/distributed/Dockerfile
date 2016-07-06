FROM continuumio/anaconda3
MAINTAINER Ben Zaitlen "ben.zaitlen@continuum.io"

# Create anaconda group and user
RUN groupadd anaconda
RUN useradd -g anaconda -d /opt/continuum anaconda
WORKDIR /tmp

ENV PATH /opt/conda/bin:$PATH

# Get latest distributed
RUN conda install dask distributed -y -q
COPY distributed_setup.sh /tmp/distributed_setup.sh
RUN chmod +x /tmp/distributed_setup.sh
RUN bash /tmp/distributed_setup.sh

# Add script: register to proxy
COPY register.py /tmp/register.py
COPY start-scheduler.sh /tmp/start-scheduler.sh
COPY start-worker.sh /tmp/start-worker.sh
RUN chown anaconda:anaconda /tmp/register.py /tmp/*.sh
RUN chmod +x /tmp/register.py /tmp/*.sh

USER anaconda

ENV APP_PORT 9002
EXPOSE 9000
EXPOSE 9001
EXPOSE 9002

CMD ["dask-scheduler"]
