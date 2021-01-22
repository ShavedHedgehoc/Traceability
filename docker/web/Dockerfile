FROM python:3.8

# Install MSSQL ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN exit
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Install pyodbc dependencies
RUN apt-get update && apt-get install -y gcc unixodbc-dev
RUN apt-get install postgresql-client -y

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt



# make db migrations
# RUN ["chmod", "+x", "./entrypoint.sh"]
# ENTRYPOINT ["./entrypoint.sh"]
# CMD python traceability.py

