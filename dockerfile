FROM python:3.10-alpine

WORKDIR /stock_products

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /stock_products

RUN pip install -r requirements.txt

COPY . /stock_products

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]