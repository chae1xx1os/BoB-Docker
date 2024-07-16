FROM python:3.11.0-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt/bbot
RUN mkdir -p /opt/bbot/conf

COPY ./*.py /opt/bbot/
COPY ./*.sh /opt/bbot/
COPY ./requirements.txt /opt/bbot/
WORKDIR /opt/bbot

RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install --upgrade pip
RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r requirements.txt

RUN chmod +x /opt/bbot/start.sh

CMD ["bash", "-c", "/opt/bbot/start.sh"]