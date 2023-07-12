FROM python:3.11.4-slim

WORKDIR /app

# Copy requirements.txt to app directory
COPY ./requirements.txt ./requirements.txt

# install requirements
RUN pip install -r requirements.txt

# Copy all files to app directory
COPY . .

EXPOSE 5000

CMD [ "bash","gunicorn.sh" ]


