# Setting up poetry project

```cmd
poetry new app_name --name app (--src)
```

* Poetry is now initialized with `pyproject.toml` file

* Now create virtul `environment` bu running
    ```terminal
    poetry install 
    ``

* Activate `virtual environment` by running 
    ```terminal
    poetry shell
    ```

* Copy the path in my case but your will be different.
    `Spawning shell within C:\Users\PC\AppData\Local\pypoetry\Cache\virtualenvs\app-bNcI04Xs-py3.11`

* Adding virtual env to vscode
    - Press `ctrl+shift+p`
    - Type `Python: Select Interpreter`
    - Select Enter interpreter path...
    - Paste the path which you have `copied` from `shell`
    - Press enter `Now you have successfully added path to your vscode of virtual env`

* Add dependencies to `pyproject.toml` file
* Install fastapi with postry 

    ```cmd 
    poetry add fastapi
    ```

* Create main.py file in your created dir in my case is `app`

```python
from fastapi import FastAPI

app : FastAPI = FastAPI()

@app.get("/")
async def root():
    return {"message": "Aqeel Shahzad"}
```

* Now run the server and check everything is working fine

```cmd
 poetry run uvicorn app.main:app --reload
```

### From now we have setup poetry project and added dependencies to it

# Now we will setup docker

* First check if you have installed docker or not by running
    ```cmd
    docker --version
    ```

* It should look something like this
    ```cmd
    Docker version 20.10.8, build 3967b7d
    ```
* Also check `client` and `server` version

It should look like something like this

```cmd
PS D:\WMD-q5-learning\class_path\class03_practice\class_03> docker version
Client:
 Cloud integration: v1.0.35+desktop.11
 Version:           25.0.3
 API version:       1.44
 Go version:        go1.21.6
 Git commit:        4debf41
 Built:             Tue Feb  6 21:13:02 2024
 OS/Arch:           windows/amd64
 Context:           default

Server: Docker Desktop 4.28.0 (139021)
 Engine:
  Version:          25.0.3
  API version:      1.44 (minimum version 1.24)
  Go version:       go1.21.6
  Git commit:       f417435
  Built:            Tue Feb  6 21:14:25 2024
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.28
  GitCommit:        ae07eda36dd25f8a1b98dfbf587313b99c0190bb
 runc:
  Version:          1.1.12
  GitCommit:        v1.1.12-0-g51d5e94
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

Note: If you are using windows then you need to enable `WSL2`

Also you have to run `Docker desktop` also docker server will not be shown

* Now we will create `Dockerfile` in root dir of our project 
* You can also name it `Dockerfile.dev`
    - past the following code in `Dockerfile`

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.12

LABEL maintainer="aqeelshahzad1215@gmail.com"


# Set the working directory in the container
WORKDIR /code

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# install poetry
RUN pip install poetry

# Copy the current directory contents into the container at /code
COPY . /code

# Configuration to avoid creating virtual environments inside the Docker container
RUN poetry config virtualenvs.create false


RUN poetry install 

# make the port accessible outside of the container for real world
EXPOSE 8000

# Run the app. CMD can be overridden when starting the container
CMD ["poetry","run","uvicorn","app.main:app","--host","0.0.0.0" ,"--reload"]
```


- Now building the image 
    - `-f` which file to use `(Docker)` filename
    - `-t` is `tag` which name of image you want to give
    - `.` mean current location of file to use for building image 
    ```cmd
    docker build -f Dockerfile.dev -t name_of_your_image .
    ```

**Check Images:**

```bash
docker images
```

**Verify the config**

```bash
docker inspect your_image_name
```

**Now check the docker images**

```bash
docker images ls
```

**Benefits:**

* **Smaller Image Size:** By copying only dependencies in the second stage, the image size remains minimal.
* **Faster Builds:** Subsequent builds only rebuild the first stage if dependencies change, leading to faster builds.
* **No Poetry in Runtime:** Poetry is not required in the final image, reducing the overall footprint.

**Additional Notes:**

* You can customize the commands and configurations based on your project's specific needs.
* Consider using `.dockerignore` to exclude unnecessary files from the build process.
* Explore advanced Docker features like environment variables and volumes for further customization.

Remember to choose the appropriate Dockerfile based on your use case, balancing development convenience with production efficiency.

## Project for You: Optimization for Production

You will now learn from this Tutorial and try to further optimize the production build:

https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

Note: BuildKit is the default builder for users on Docker Desktop, and Docker Engine as of version 23.0 and above therefore no need to add this in our Dockerfile as mentioned in this tutorial.


## References

## What Are Multi-Stage Docker Builds?

**Multi-stage builds** are a powerful feature in Docker that allow you to create more efficient and smaller container images. They are particularly useful when optimizing Dockerfiles while keeping them readable and maintainable.

In a nutshell, multi-stage builds involve using multiple `FROM` statements in your Dockerfile. Each `FROM` instruction defines a new stage in the build process. You can selectively copy artifacts from one stage to another, leaving behind anything you don't need in the final image.



### How Do Multi-Stage Builds Work?

https://devguide.dev/blog/how-to-create-multi-stage-dockerfile

### What is BuildKit

BuildKit is an improved backend to replace the legacy builder. BuildKit is the default builder for users on Docker Desktop, and Docker Engine as of version 23.0.

