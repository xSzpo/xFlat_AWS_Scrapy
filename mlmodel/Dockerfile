# Use an official Python runtime as a parent image
# docker build -t app_mlmodel:0.0.2 .
# docker run -it python:3.7-alpine /bin/ash
# docker run -it python:3.7.2-slim bash
# docker exec -it <container-name/ID> bash
#FROM python:3.6-slim

FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update \
    && apt-get install libgomp1
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8666 8000

# run
CMD ["python", "-u","/app/fastapi_main.py"]
