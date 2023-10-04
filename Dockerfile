# pull official base image
FROM python:3.11.4-slim-buster

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# download asent model
RUN python -m spacy download en_core_web_lg

# copy project's files
COPY ciphixanalyzer /ciphixanalyzer
WORKDIR /ciphixanalyser

EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "/ciphixanalyzer/manage.py", "runserver", "0.0.0.0:8000"]
