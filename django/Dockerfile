# pull official base image
FROM python:3.10.6-alpine

# set work directory
#WORKDIR /app

# needed because permissions (if created by docker => root)
ENV HOME=/app
ENV APP_HOME=/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME


# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add gcc musl-dev mariadb-connector-c-dev gettext

RUN apk --update --no-cache add curl

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#RUN apk del build-deps

# copy project
COPY . .

# Entry point performs:
# - migrate
# - collect static
# - compile translations
# - launch gunicorn

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
#ENTRYPOINT ["/docker-entrypoint.sh"]
