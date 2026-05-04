#build de l'app
FROM node:20-alpine AS build-stage


WORKDIR /app

#install des dep
COPY package*.json ./
RUN npm install

COPY . .


RUN npm run generate

# Serveur 
FROM nginx:stable-alpine


RUN rm -rf /usr/share/nginx/html/*

# copie fichier vers ngnix
COPY --from=build-stage /app/.output/public /usr/share/nginx/html


EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

