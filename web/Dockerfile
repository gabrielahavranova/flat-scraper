FROM python:3

COPY server.py /

COPY requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=server.py

CMD python -m flask run --host=0.0.0.0 -p 8080
