FROM continuumio/anaconda3
MAINTAINER Min RK "benjaminrk@gmail.com"

# Create anaconda group and user
RUN groupadd anaconda
RUN useradd -g anaconda -m -d /opt/continuum anaconda
WORKDIR /tmp

ENV PATH /opt/conda/bin:$PATH

# Get latest ipyparallel
RUN conda install -c conda-forge ipyparallel -y -q

# Add script: register to proxy
COPY start-controller.sh /tmp/start-controller.sh
COPY start-worker.sh /tmp/start-worker.sh
COPY profile /tmp/profile
RUN chown -R anaconda:anaconda /tmp/*.sh /tmp/profile
RUN chmod +x /tmp/*.sh

USER anaconda
RUN mkdir -p $(ipython locate profile) \
 && rsync -aru /tmp/profile/ $(ipython locate profile)/

EXPOSE 10000 \
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

CMD ["false"]
