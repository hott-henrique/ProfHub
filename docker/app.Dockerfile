FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update
RUN apt install -y python3.11 python3.11-dev python3-pip

WORKDIR /usr/src/app

COPY app/requirements.txt requirements.txt
COPY .streamlit /usr/src/app/.streamlit

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

SHELL [ "/bin/bash", "-c"]

CMD [ "streamlit", "run", "app/app.py" ]
