FROM python:3.12.0

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN python ./Backend/manage.py makemigrations
RUN python ./Backend/manage.py migrate

CMD ["python", "./Backend/manage.py", "runserver", "0.0.0.0:8000"]
