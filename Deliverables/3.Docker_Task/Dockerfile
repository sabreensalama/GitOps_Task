FROM postman/newman:5.3-alpine

ENV NODE_PATH=/usr/local/lib/node_modules

WORKDIR /etc/newman

RUN apk update && \
    apk upgrade && \
    apk add --no-cache curl zip iputils && \
    npm install -g newman-reporter-csvallinone && \
    rm -rf /var/cache/apk/*
    
RUN printf "nameserver 8.8.8.8\nnameserver 1.1.1.1\n" > /etc/resolv.conf

ENTRYPOINT ["newman"]

