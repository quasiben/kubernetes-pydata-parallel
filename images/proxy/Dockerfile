FROM node:6

RUN git clone https://github.com/quasiben/configurable-http-proxy.git
WORKDIR /configurable-http-proxy
RUN git checkout fix/fowards_args

EXPOSE 80
EXPOSE 81
EXPOSE 443

COPY ssl-cert.pem /tmp/ssl-cert.pem
COPY ssl-key.pem /tmp/ssl-key.pem
COPY startup.sh /usr/bin/startup.sh 
RUN chmod +x /usr/bin/startup.sh
CMD /usr/bin/startup.sh
#COPY server.js /tmp/server.js
#CMD node /tmp/server.js
