FROM python:3.9.1-alpine

RUN apk add --update --no-cache \
    build-base \
    python-dev \
    zlib-dev \
    libxml2-dev \
    libxslt-dev \
    openssl-dev \
    libffi-dev

COPY settings/requirements.txt /tmp/requirements.txt
COPY settings/libtdsodbc.0.so /usr/local/lib/libtdsodbc.0.so
RUN pip install -r /tmp/requirements.txt

ADD ./webiner_list /usr/src/webiner_list
COPY settings/exec.sh /usr/src/exec.sh
WORKDIR /usr/src/webiner_list

ENTRYPOINT ["/bin/ash"]
CMD ["/usr/src/exec.sh"]