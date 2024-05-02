FROM python:3.12 
# LABEL maintainer="aqeelshahzad1215@gmail.com"
WORKDIR /c5
# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN poetry install

# Copy the current directory code into the container /c5
COPY . /c5/

# Configuration to avoid creating virtual envirmment inside the docker container
RUN poetry config virtualenvs.create false

# Make the port available to the world at 8000
EXPOSE 8000

# Run the uvicorn server with CMD
CMD [ "poetry" , "run" , "uvicorn","app.main:app" , "--host","0.0.0.0" , "--reload"]