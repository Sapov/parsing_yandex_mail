# pull official base image
FROM python:3.9.6-alpine
#SHELL ["/bin/bash", "-c"]

# set work directory
WORKDIR /django

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

COPY --chown=django:django . .

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
#RUN useradd -rms /bin/bash django && chmod 777 /opt /run
#USER django
CMD ["gunicorn","-b","0.0.0.0:8000","mysite.wsgi:application"]
# copy project
