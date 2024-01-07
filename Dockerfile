FROM python:3.7.9

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y libsasl2-dev libldap2-dev && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]