# objective: Create image for Flask App
# build: docker build -t blog_app:latest .
# start: docker run -d -p 5000:5000 blog_app:latest

FROM python:3.6

LABEL maintainer "Nathan <...>"

RUN mkdir app

COPY .  /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

EXPOSE 5000

CMD ["python", "manage.py", "runserver","--host","0.0.0.0"]
# ENTRYPOINT ["python"]
# CMD ["app.py"]
