FROM postgres:15-alpine


ENV POSTGRES_DB=ma_db
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=password


COPY creation_request.sql /docker-entrypoint-initdb.d/