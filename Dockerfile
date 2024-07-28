FROM ubuntu:22.04

COPY code /app/code
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install python3-venv python3-pip
RUN python3 -m venv my-venv  && my-venv/bin/pip install -r requirements.txt


ENTRYPOINT [ "my-venv/bin/python3" ]
CMD [ "main.py" ]
