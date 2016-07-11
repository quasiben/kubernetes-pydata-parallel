FROM continuumio/anaconda3
MAINTAINER Ben Zaitlen "ben.zaitlen@continuum.io"

# Create anaconda group and user
RUN groupadd anaconda
RUN useradd -g anaconda -d /opt/conda anaconda
WORKDIR /tmp

# Download JAVA
RUN apt-get update \
    && apt-get install -y openjdk-7-jre-headless \
    && apt-get clean

ENV PATH /opt/conda/bin:$PATH

# Get latest distributed
RUN conda install joblib snakeviz ujson dask distributed bokeh -y -q
RUN pip install fakestockdata
RUN conda install -c conda-forge ipyparallel -y -q
COPY distributed_setup.sh /tmp/distributed_setup.sh
RUN chmod +x /tmp/distributed_setup.sh
RUN bash /tmp/distributed_setup.sh

# Set up spark
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre
ENV JRE_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre
RUN conda install -c quasiben spark -y -q
RUN curl -o /opt/conda/share/spark/jars/hadoop-aws-2.6.0.jar http://search.maven.org/remotecontent?filepath=org/apache/hadoop/hadoop-aws/2.6.0/hadoop-aws-2.6.0.jar

# setup ipyparallel
COPY profile /tmp/profile
RUN chown -R anaconda:anaconda /tmp/*.sh /tmp/profile

# Add script: register to proxy
COPY register.py /tmp/register.py
COPY start-scheduler.sh /tmp/start-scheduler.sh
COPY start-worker.sh /tmp/start-worker.sh
RUN chown anaconda:anaconda /tmp/register.py /tmp/*.sh
RUN chmod +x /tmp/register.py /tmp/*.sh
#RUN chown anaconda:anaconda -R /opt/conda


# setup for notebook
RUN mkdir /opt/app
RUN chown anaconda:anaconda -R /opt/app


#USER anaconda
RUN mkdir -p $(ipython locate profile) \
 && rsync -aru /tmp/profile/ $(ipython locate profile)/

EXPOSE 7077 \
       8080 \
       8081 \
       9001 \
       9002 \
       10000 \
       10001 \
       10002 \
       10003 \
       10004 \
       10005 \
       10101 \
       10102 \
       10103 \
       10104 \
       10105 \
       10106


CMD ["dask-scheduler"]
