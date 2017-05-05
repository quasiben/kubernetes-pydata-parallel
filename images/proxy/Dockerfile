FROM node:7

RUN npm update
RUN git clone https://github.com/jupyterhub/configurable-http-proxy.git
WORKDIR /configurable-http-proxy

EXPOSE 80
EXPOSE 81
EXPOSE 443

#COPY ssl-cert.pem /tmp/ssl-cert.pem
#COPY ssl-key.pem /tmp/ssl-key.pem
COPY startup.sh /usr/bin/startup.sh
RUN chmod +x /usr/bin/startup.sh
CMD /usr/bin/startup.sh
#COPY server.js /tmp/server.js
#CMD node /tmp/server.js
