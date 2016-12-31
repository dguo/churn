FROM python:3.6.0

RUN mkdir /usr/src/churn
WORKDIR /usr/src/churn

COPY requirements.txt setup.py ./
RUN pip install --editable .

CMD /bin/bash

