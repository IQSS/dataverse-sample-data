FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY data data/
COPY *.py *.py.sample ./
RUN mv dvconfig.py.sample dvconfig.py

CMD [ "python", "./create_sample_data.py" ]
