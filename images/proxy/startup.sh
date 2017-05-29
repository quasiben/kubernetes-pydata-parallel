npm install
 ./bin/configurable-http-proxy --port 443 --redirect-port 80 --ip 0.0.0.0 --api-ip 0.0.0.0 --api-port 81 --ssl-key=/tmp/ssl-key.pem --ssl-cert=/tmp/ssl-cert.pem --ssl-allow-rc4 --log-level debug
#./bin/configurable-http-proxy --port 80 --api-port 81 --api-ip 0.0.0.0 --no-x-forward  --log-level debug
# node /tmp/server.js
