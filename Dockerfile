# Use an official Python runtime as a parent image
FROM python:3.11

# set the working directory in the container
WORKDIR /nlp_app/

# Copy the current directory contents into the containe at /nlp_app
COPY . .

RUN apt-get update && apt-get install -y postgresql-client

# Install Python dependencies
RUN pip install -r requirements.txt

# Make port 8000 available
EXPOSE 8000

# Command to run Gunicorn app
CMD ["gunicorn -c gunicorn_config.py main:main_app"]