FROM node:6

RUN npm install -g configurable-http-proxy

EXPOSE 80
EXPOSE 81

COPY startup.sh /usr/bin/startup.sh
RUN chmod +x /usr/bin/startup.sh
CMD "startup.sh"
