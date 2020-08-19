FROM alpine:3.7
#
RUN apk add --no-cache g++ freetype-dev jpeg-dev zlib-dev
RUN apk add --no-cache alpine-sdk linux-headers libxml2-dev gcc musl-dev python3-dev libffi-dev openssl-dev

RUN apk add --no-cache python3 uwsgi-python && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD python3 /app/backend-py/manage.py runserver
