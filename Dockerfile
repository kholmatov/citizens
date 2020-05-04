# base image
FROM python:3.7 as builder

# Create virtualenv
RUN python3.7 -m venv /usr/share/python3/app
ENV PATH="/usr/share/python3/app/bin:${PATH}"

# Speed up build
ADD requirements*.txt /tmp/
RUN pip install --no-cache-dir -Ur /tmp/requirements.txt

########################################################################
# CI image
FROM builder as tests
RUN pip install --no-cache-dir -Ur /tmp/requirements.tests.txt
ENV TOXDIR=/tmp

########################################################################
# Image with app installed
FROM builder as app

ADD citizens/ /mnt/citizens/
ADD db/ /mnt/citizens/
ADD utils/ /mnt/citizens/
ADD app.py /mnt/citizens/

RUN pip install --no-cache-dir -Ur /tmp/requirements.txt

SHELL ["/bin/bash", "-c"]
WORKDIR /mnt

EXPOSE 8080

CMD ["python3", "app.py"]
