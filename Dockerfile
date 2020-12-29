FROM python:3.9.1-buster

RUN apt update && apt -y install gcc unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc
COPY settings/requirements.txt /tmp/requirements.txt
COPY settings/odbcinst.ini /etc/odbcinst.ini
RUN pip install -r /tmp/requirements.txt

ADD ./webiner_list /usr/src/webiner_list
COPY settings/exec.sh /usr/src/exec.sh
WORKDIR /usr/src/webiner_list

RUN export ODBCINI=/etc/odbc.ini && \
    export ODBCSYSINI=/etc && \
    export FREETDSCONF=/etc/freetds/freetds.conf

ENTRYPOINT ["/bin/bash"]
CMD ["/usr/src/exec.sh"]