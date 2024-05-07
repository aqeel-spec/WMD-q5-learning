# Todo app

- App created using following tech
    - `Fastapi`
    - `Docker`
    - `dev container` for development purpose
    - `docker compose` create compose.yaml file to automate docker
    - `postgres` as database

**Create docker file**
* Initial configuration for docker file
    - Create `Dockerfile` in your project

```bash
FROM python:3.12

WORKDIR /todo

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ADD pyproject.toml /todo

ADD ./app /todo

RUN pip install poetry

# disable virtualenv creation
RUN poetry config virtualenvs.create false

RUN poetry install

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Create docker compose file**

* create `compose.yaml` file
   - configure it to use api image and db

This will create 2 container connected to each other with same network

```bash
docker compose up -d
```

