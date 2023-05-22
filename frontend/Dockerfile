FROM node:20-alpine3.16
LABEL maintainer="n_bul"

WORKDIR /app
COPY package*.json /app

RUN npm install

COPY . ./app

EXPOSE 3000

CMD ["npm", "start"]
