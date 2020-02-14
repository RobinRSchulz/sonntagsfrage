FROM ubuntu:18.04

# -y = always yes
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

WORKDIR /app

#copying server.py and getData.py
COPY ../server.py .
COPY ../getData.py .
COPY ../static/ .
COPY ../templates/ .

# TODO choose dir structure (/app/?)
#COPY ./requirements.txt WORKDIR/requirements.txt
ENTRYPOINT [ "python" ]
# todo start cron job (or whatever): getData.py
CMD [ "server.py" ]


