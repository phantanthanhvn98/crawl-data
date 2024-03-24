FROM python:3.12.2

LABEL authors="phantanthanh"

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.58/linux64/chrome-linux64.zip
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/
RUN rm -f /tmp/chromedriver.zip

# set display port to avoid crash
ENV DISPLAY=:99

ADD requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN rm -f ./requirements.txt

RUN pip install --upgrade scrapy itemloaders

ADD . ./src

WORKDIR ./src

ENTRYPOINT []