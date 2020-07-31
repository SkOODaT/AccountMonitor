FROM python:3.7-slim
WORKDIR /accountmonitor
COPY requirements.txt /accountmonitor
RUN pip install -r requirements.txt
COPY . /accountmonitor
ENTRYPOINT ["python"]
