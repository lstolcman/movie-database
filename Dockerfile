FROM python:3.7-alpine

RUN adduser -D moviedb

WORKDIR /home/moviedb

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY moviedb.py config.py schema.py ./

ENV FLASK_APP moviedb.py

RUN chown -R moviedb:moviedb ./
USER moviedb

EXPOSE 5000
RUN python schema.py
CMD ["gunicorn", "-b", ":5000", "moviedb:app"]

