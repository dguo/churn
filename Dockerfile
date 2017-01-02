FROM python:3.5.2

RUN mkdir /usr/src/churn
WORKDIR /usr/src/churn

COPY setup.py requirements-dev.txt ./
RUN pip install --editable . -r requirements-dev.txt

CMD /bin/bash

