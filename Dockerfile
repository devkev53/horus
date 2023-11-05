FROM python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /

COPY requirements.txt /

RUN apt-get update
RUN apt-get install -y libpq-dev python-dev-is-python3

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

COPY /build/index.html /templates

EXPOSE 8000

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh" ]

# COPY ./build