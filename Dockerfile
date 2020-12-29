FROM python:3.9.1-buster

RUN apt update && apt -y install gcc unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc
COPY settings/requirements.txt /tmp/requirements.txt
COPY settings/odbcinst.ini /etc/odbcinst.ini
COPY settings/odbc.ini /etc/odbc.ini
RUN pip install -r /tmp/requirements.txt

ADD ./webiner_list /usr/src/webiner_list
COPY settings/exec.sh /usr/src/exec.sh
WORKDIR /usr/src/webiner_list

ENTRYPOINT ["/bin/bash"]
CMD ["/usr/src/exec.sh"]