FROM python:3.6-slim

LABEL maintainer="shikanon"
LABEL email="<shikanon@tensorbytes.com>"

COPY . /home/sota
WORKDIR /home/sota

RUN apt update && apt install gcc -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple/

RUN chmod +x ./run.sh

EXPOSE 8000


CMD [ "./run.sh" ]