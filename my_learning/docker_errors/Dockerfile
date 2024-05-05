FROM python:3.12

WORKDIR /code

RUN rm -rf /var/lib/apt/lists/*

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# COPY . /code/

ADD ../pyproject.toml  /code/
ADD ./app /code/app

RUN pip install poetry

# Configuration to avoid creating virtual environments inside the Docker container
RUN poetry config virtualenvs.create false



RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]