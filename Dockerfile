FROM joyzoursky/python-chromedriver:3.7

RUN pip install selenium

COPY coxusage.py /usr/bin/coxusage.py

CMD [ "python", "/usr/bin/coxusage.py" ]