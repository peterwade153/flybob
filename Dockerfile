FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY scripts/ /code/
RUN chmod +x scripts/start.sh
EXPOSE 5000
CMD bash -c scripts/start.sh