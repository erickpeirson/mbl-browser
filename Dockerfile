FROM python:3
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim
ARG PROJECT=mbl
ARG PROJECT_DIR=/var/www/${PROJECT} 
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
RUN git clone -b task/MHDP-25  https://github.com/diging/mbl-browser.git
WORKDIR $PROJECT_DIR/mbl-browser
RUN pip install -r requirements.txt

ENV DJANGO_SECRET_KEY=lk&b)9bfq@5kxb_c*zrko-g-de8gm9mwpucjq1^z=1o2u!-3a)
ENV DATABASE_URL=postgres://mbl:mbl@host.docker.internal:5432/mbl
ENV DEBUG=True
RUN python manage.py migrate

EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

