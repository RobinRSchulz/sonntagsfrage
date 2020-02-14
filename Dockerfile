FROM ubuntu:18.04

# -y = always yes
RUN apt-get update -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

#copying server.py and getData.py
COPY server.py .
COPY getData.py .
COPY static/ static
COPY templates/ templates

# python deps
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#make sure some data is present
RUN python3 getData.py

ENTRYPOINT [ "python3" ]
# todo start cron job (or whatever): getData.py
CMD [ "server.py" ]
