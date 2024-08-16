FROM python:3.11.0-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt/chatbot
RUN mkdir -p /opt/chatbot/conf

COPY ./*.py /opt/chatbot/
COPY ./*.sh /opt/chatbot/
COPY ./requirements.txt /opt/chatbot/
WORKDIR /opt/chatbot

RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install --upgrade pip
RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r requirements.txt

RUN chmod +x /opt/chatbot/start.sh

CMD ["bash", "-c", "/opt/chatbot/start.sh"]