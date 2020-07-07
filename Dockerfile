# use the alpine image with selenium because it's smaller
FROM joyzoursky/python-chromedriver:3.8-alpine3.10-selenium

# copy the script
COPY coxusage.py /usr/bin/coxusage.py

# prepare command that runs coxusage when the image is executed
CMD [ "python", "/usr/bin/coxusage.py" ]