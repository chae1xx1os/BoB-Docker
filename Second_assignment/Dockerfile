# Node.js를 사용하여 Tailwind CSS를 빌드하는 단계
FROM node:16-alpine AS tailwind-builder
WORKDIR /app
COPY ./static ./static
RUN npm install -D tailwindcss postcss autoprefixer
RUN npx tailwindcss -i ./static/src/styles.css -o ./static/dist/styles.css --minify

# Python 이미지를 사용하여 FastAPI를 설정하는 단계
FROM python:3.11.0-slim
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt/chatbot
RUN mkdir -p /opt/chatbot/templates
RUN mkdir -p /opt/chatbot/static

COPY ./*.py /opt/chatbot/
COPY ./*.sh /opt/chatbot/
COPY ./requirements.txt /opt/chatbot/
COPY ./templates /opt/chatbot/templates/
COPY --from=tailwind-builder /app/static /opt/chatbot/static/

WORKDIR /opt/chatbot

RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install --upgrade pip
RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r /opt/chatbot/requirements.txt

RUN chmod +x /opt/chatbot/start.sh

CMD ["bash", "-c", "/opt/chatbot/start.sh"]
