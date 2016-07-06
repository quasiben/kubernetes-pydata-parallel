FROM gcr.io/continuum-compute/miniconda-base:v11

COPY environment.yml /opt/continuum/environment.yml
RUN conda env create -f /opt/continuum/environment.yml

ENV PATH /opt/continuum/anaconda/envs/scipy-demo/bin:$PATH

RUN mkdir /opt/continuum/app
COPY core /opt/continuum/app/core
COPY start.py /opt/continuum/app/start.py
USER root
RUN chmod +x /opt/continuum/app/start.py
USER anaconda

EXPOSE 8080

CMD ["python", "/opt/continuum/app/start.py"]
