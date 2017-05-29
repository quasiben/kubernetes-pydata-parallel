FROM centos:7

ENV LANG en_US.UTF-8

RUN yum update -y \
    && yum install -y tar git make bzip2 epel-release \
    && yum install -y nginx \
    && yum clean all

COPY nginx.conf /etc/nginx/conf.d/nginx.conf
 
# Create anaconda group and user
RUN groupadd anaconda
RUN useradd -g anaconda -d /opt/continuum anaconda
USER anaconda
WORKDIR /opt/continuum

# Conda setup
RUN curl -s -L https://repo.continuum.io/miniconda/Miniconda3-4.0.5-Linux-x86_64.sh -o /opt/continuum/miniconda.sh \
    && bash /opt/continuum/miniconda.sh -b -p /opt/continuum/anaconda \
    && rm /opt/continuum/miniconda.sh \
    && /opt/continuum/anaconda/bin/conda clean -y -a

ENV PATH /opt/continuum/anaconda/bin:$PATH
RUN conda config --set show_channel_urls True

# Add script: register to proxy
RUN mkdir /opt/continuum/scripts/
COPY register.py /opt/continuum/scripts//register.py
USER root
RUN chown anaconda:anaconda /opt/continuum/scripts/register.py
USER anaconda
 

COPY environment.yml /opt/continuum/environment.yml
RUN conda env create -f /opt/continuum/environment.yml

ENV PATH /opt/continuum/anaconda/envs/scipy-demo/bin:$PATH

RUN mkdir /opt/continuum/app
COPY core /opt/continuum/app/core
COPY start.py /opt/continuum/app/start.py
USER root
RUN chmod +x /opt/continuum/app/start.py

COPY pycon-parallel-cert.pem /tmp/ssl-cert.pem 
COPY pycon-parallel-key.pem /tmp/ssl-key.pem

EXPOSE 8080
EXPOSE 8081

RUN /usr/sbin/nginx

user anaconda
CMD ["python", "/opt/continuum/app/start.py"]
