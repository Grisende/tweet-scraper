FROM python:3.12

RUN python3 -m venv .venv
RUN . .venv/bin/activate
RUN pip3 install flask

RUN mkdir -p /var/www/twitter-scraper
COPY ./requirements.txt /var/www/twitter-scraper/requirements.txt

WORKDIR /var/www/twitter-scraper

USER root

RUN apt-get update \ 
  && apt-get install htop -y \
  && apt-get install libnss3 -y \
  && apt-get install chromium -y

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0"]