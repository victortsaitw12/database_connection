FROM python:3.7
#FROM ubuntu:16.04

RUN apt-get clean && apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    export LANGUAGE=en_US.UTF-8 && \
    export LANG=en_US.UTF-8 && \
    export LC_ALL=en_US.UTF-8

RUN dpkg-reconfigure locales
#RUN update-locale LANG=en_US.UTF-8

ENV ORACLE_HOME=/usr/lib/oracle/12.1/client64
ENV PATH=$PATH:$ORACLE_HOME/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME/lib

# ORACLE
RUN git clone https://github.com/dddpaul/docker-oracleclient.git
RUN apt-get update && \
    apt-get -y install alien libaio1 vim && \
    alien -i /docker-oracleclient/oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm && \
    alien -i /docker-oracleclient/oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm && \
    alien -i /docker-oracleclient/oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm && \
    ln -snf /usr/lib/oracle/12.1/client64 /opt/oracle && \
    pip install cx_oracle

# MSSQL
RUN apt-get install -y curl apt-transport-https gnupg2 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools && \
    apt-get install unixodbc-dev && \
    pip install pyodbc

ENV MSSQL_HOME=/opt/mssql-tools/bin
ENV PATH=$PATH:MSSQL_HOME

# MYSQL
RUN pip install pymysql

#Django
RUN pip install django
# Grafana
RUN wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.1.4_amd64.deb
RUN apt-get install -y adduser libfontconfig
RUN dpkg -i grafana_5.1.4_amd64.deb
RUN grafana-cli plugins install grafana-simple-json-datasource
RUN grafana-cli plugins install grafana-piechart-panel

RUN apt-get install -y mysql-client
