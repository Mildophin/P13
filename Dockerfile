FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD gunicorn --bind 0.0.0.0:$PORT config.wsgi