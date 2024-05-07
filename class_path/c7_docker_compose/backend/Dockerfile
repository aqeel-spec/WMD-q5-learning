FROM python:3.12

LABEL maintainer="aqeelshahzad1215@gmail.com"

WORKDIR /todo_app

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ADD pyproject.toml .env /todo_app/
ADD ./app /todo_app/app

RUN pip install poetry

# disable virtualenv creation
RUN poetry config virtualenvs.create false

RUN poetry install

EXPOSE 8000

CMD [ "poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

