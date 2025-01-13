FROM python:3.12
COPY . /opt/app
WORKDIR /opt/app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","run.py"]