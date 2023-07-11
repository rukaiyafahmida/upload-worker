FROM python:3.11.4-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt to app directory
COPY ./requirements.txt ./requirements.txt

# install requirements
RUN pip install -r requirements.txt

# Copy all files to app directory
COPY . .


EXPOSE 5000

CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info