FROM python:3.9.1-alpine3.12

RUN apk add --update --no-cache \
    mkdir /usr/src/webiner_list

COPY settings/requirements.txt /tmp/requirements.txt
COPY settings/libtdsodbc.0.so /usr/local/lib/libtdsodbc.0.so
RUN pip install -r /tmp/requirements.txt \
    rm /tmp/requirements.txt

COPY ./webiner_list /usr/src/webiner_list
COPY settings/exec.sh /usr/src/exec.sh
WORKDIR /usr/src/webiner_list

ENTRYPOINT ["/bin/ash"]
CMD ["/usr/src/exec.sh"]