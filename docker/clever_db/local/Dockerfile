FROM mcr.microsoft.com/mssql/server:2017-latest


RUN mkdir -p /usr/work
WORKDIR /usr/work
COPY ./ /usr/work 
RUN mkdir -p /usr/config
WORKDIR /usr/config
# COPY ./docker/clever_db /usr/config
# For docker run
COPY ./ /usr/config 
RUN ["chmod", "+x", "/usr/config/entrypoint.sh"]
RUN ["chmod", "+x", "/usr/config/configure-db.sh"]
ENTRYPOINT ["./entrypoint.sh"]

expose 1433
# CMD /bin/bash ./entrypoint.sh


