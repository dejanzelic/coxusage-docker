FROM python:3.8-alpine

# install chromedriver
RUN apk update 
RUN apk add python3-dev gcc libc-dev libffi-dev
RUN apk add chromium chromium-chromedriver

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium
RUN pip install selenium-stealth

COPY coxusage.py /usr/bin/coxusage.py

CMD [ "python", "/usr/bin/coxusage.py" ]