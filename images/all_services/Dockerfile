FROM continuumio/miniconda3:4.1.11
MAINTAINER Ben Zaitlen "quasiben@gmail.com"

# Create anaconda group and user
RUN groupadd anaconda
RUN useradd -g anaconda -d /opt/conda anaconda
WORKDIR /tmp

# Download JAVA
RUN apt-get update \
    && apt-get install -y vim openjdk-7-jre-headless graphviz\
    && apt-get clean

ENV PATH /opt/conda/bin:$PATH

# Install Base Anaconda 3.5
RUN conda install anaconda python=3.5 -y -q

# Get latest notebook
RUN conda install notebook 

# Get base distributed/bokeh
RUN conda install joblib snakeviz ujson dask distributed bokeh pandas-datareader -y -q
RUN conda install -c conda-forge dask distributed s3fs -y -q
RUN pip install fakestockdata graphviz

# setup ipyparallel
COPY profile /tmp/profile

# Add script: register to proxy
COPY register.py /tmp/register.py
COPY start-scheduler.sh /tmp/start-scheduler.sh
COPY start-worker.sh /tmp/start-worker.sh
RUN chown -R anaconda:anaconda /tmp/register.py /tmp/*.sh /tmp/profile
RUN chmod +x /tmp/register.py /tmp/*.sh

# Get github distributed 
RUN conda remove distributed --force -y -q
RUN git clone https://github.com/dask/distributed.git
RUN cd distributed; python setup.py install

# Get github bokeh
RUN conda remove bokeh --force -y -q
RUN conda install -c bokeh nodejs -y -q
RUN git clone https://github.com/bokeh/bokeh.git
RUN cd bokeh/bokehjs; npm install
RUN cd bokeh; python setup.py install --build-js
COPY app_index.html /opt/conda/lib/python3.5/site-packages/bokeh-0.12.7.dev10+9.g90b941d-py3.5.egg/bokeh/server/views/app_index.html

# Set up spark
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre
ENV JRE_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre
RUN conda install -c conda-forge py4j=0.10.4 -y -q
RUN conda install -c quasiben pyspark=2.1.1 -y 
RUN curl -o /opt/conda/lib/python3.5/site-packages/pyspark/jars/hadoop-aws-2.7.3.jar  https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar
RUN curl -o /opt/conda/lib/python3.5/site-packages/pyspark/jars/aws-java-sdk-1.7.4.2.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.4.2/aws-java-sdk-1.7.4.2.jar
COPY spark-defaults.conf /opt/conda/share/spark/conf/spark-defaults.conf
ENV SPARK_CONF_DIR /opt/conda/share/spark/conf
ENV SPARK_HOME /opt/conda/lib/python3.5/site-packages/pyspark
RUN cp -r /opt/conda/sbin $SPARK_HOME
RUN mkdir -p $SPARK_HOME/launcher/target/scala-2.11


# setup for notebook
RUN mkdir -p /opt/app/parallel-tutorial
RUN mkdir -p /opt/app/dask-tutorial

# setup prep for pydata-parallel
RUN git clone https://github.com/pydata/parallel-tutorial.git /opt/app/parallel-tutorial
RUN cd /opt/app/pydata-parallel && python prep.py

# setup prep dask-tutorial
RUN git clone https://github.com/dask/dask-tutorial.git /opt/app/dask-tutorial
RUN cd /opt/app/pydata-parallel && git checkout scipy-2017

RUN chown anaconda:anaconda -R /opt/app
RUN chown anaconda:anaconda -R /opt/conda


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

USER anaconda

RUN git clone https://github.com/jcrist/dask-tutorial-pydata-seattle-2017 /tmp/ask-tutorial-pydata-seattle-2017
RUN cp -r /tmp/ask-tutorial-pydata-seattle-2017/* /opt/app/

ENV SHELL /bin/bash

CMD ["dask-scheduler"]
