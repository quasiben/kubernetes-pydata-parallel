FROM continuumio/anaconda3
MAINTAINER Ben Zaitlen "ben.zaitlen@continuum.io"

# Create anaconda group and user
RUN groupadd anaconda
RUN useradd -g anaconda -d /opt/continuum anaconda
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

# Add script: register to proxy
COPY register.py /tmp/register.py
COPY start-spark-master.sh /tmp/start-spark-master.sh
COPY start-spark-worker.sh /tmp/start-spark-worker.sh
RUN chown anaconda:anaconda /tmp/register.py /tmp/*.sh
RUN chmod +x /tmp/register.py /tmp/*.sh
RUN chown anaconda:anaconda -R /opt/conda

USER anaconda

ENV APP_PORT 7000
EXPOSE 7077
EXPOSE 8080
EXPOSE 8081
CMD ["python", "-m", "http.server"]
