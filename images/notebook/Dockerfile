FROM continuumio/anaconda3
MAINTAINER Ben Zaitlen "ben.zaitlen@continuum.io"

# Create anaconda group and user
RUN groupadd anaconda
RUN useradd -g anaconda -d /opt/conda anaconda
WORKDIR /tmp

ENV PATH /opt/conda/bin:$PATH

# Download JAVA
RUN apt-get update \
    && apt-get install -y openjdk-7-jre-headless \
    && apt-get clean

ENV JAVA_HOME /etc/alternatives/jre_1.7.0
ENV JRE_HOME /etc/alternatives/jre_1.7.0

# Get latest spark
RUN conda install -c quasiben spark -y -q

# Get latest distributed
RUN conda install dask distributed -y -q
COPY distributed_setup.sh /tmp/distributed_setup.sh
RUN chmod +x /tmp/distributed_setup.sh
RUN bash /tmp/distributed_setup.sh

# Get IPython parallel
RUN conda install -c conda-forge ipyparallel -y -q

# Add script: register to proxy
COPY register.py /tmp/register.py
COPY startup.sh /tmp/startup.sh
RUN chown anaconda:anaconda /tmp/register.py /tmp/*.sh
RUN chmod +x /tmp/register.py /tmp/*.sh
# add IPython profile files
COPY profile /opt/conda/.ipython/profile_default
RUN chown anaconda:anaconda -R /opt/conda

RUN mkdir /opt/app
RUN chown anaconda:anaconda -R /opt/app

USER anaconda

ENV APP_PORT 8080

CMD ["python", "-m", "http.server"]
