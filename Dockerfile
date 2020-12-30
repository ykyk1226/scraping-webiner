FROM python:3.9.1-buster

RUN apt update && \
    apt -y install gcc=4:8.3.0-1 \
                   unixodbc=2.3.6-0.1 \
                   unixodbc-dev=2.3.6-0.1 \
                   freetds-dev=1.00.104-1+deb10u1 \
                   freetds-bin=1.00.104-1+deb10u1 \
                   tdsodbc=1.00.104-1+deb10u1 && \
    export ODBCINI=/etc/odbc.ini && \
    export ODBCSYSINI=/etc && \
    export FREETDSCONF=/etc/freetds/freetds.conf

COPY settings/requirements.txt /tmp/requirements.txt
COPY settings/odbcinst.ini /etc/odbcinst.ini
RUN pip install -r /tmp/requirements.txt

ADD ./webiner_list /usr/src/webiner_list
COPY settings/exec.sh /usr/src/exec.sh
WORKDIR /usr/src/webiner_list

# spiderを追加した場合はexec.shに追加
ENTRYPOINT ["/bin/bash"]
CMD ["/usr/src/exec.sh"]