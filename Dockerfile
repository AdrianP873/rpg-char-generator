FROM python:3.8

# Setting application work directory
WORKDIR /usr/src/app

# Install application requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy application files to the container working directory
COPY ./application ./

EXPOSE 5000

# Run application
CMD python application.py
