# Fastapi codebase 

**Docker Installations**

* Windows
    - `WSL`  with `Docker Desktop`
* `Mac`
    - `Docker Desktop`
* `Linux`
    - `Docker`

**Dockerfile** write

```bash
docker build -t ImageName:tag .
```

If you have `Dockerfile` with customize name like `Dockerfile.dev` then use

```bash
docker build -f Dockerfile.dev -t ImageName:tag .
```

**Docker Run**

Run the container
```bash
docker run -d -p 8000:8000 ImageName:tag
```

```bash
docker images
```

```bash
docker image ls
```

Show list of running containers

```bash
docker ps
```

Shows all contaienrs either stop or running

```bash
docker container ls
```

```bash
docker ps -a
```

```bash
docker container ls -a
```


- **Image**
    - Rest Form
- **Container**
    - `CPU` or `RAM` begins to utilize

Check docker is working properly

```bash
docker run hello-world
```

### Here is link how to create todo app with neon database
    https://neon.tech/blog/deploy-a-serverless-fastapi-app-with-neon-postgres-and-aws-app-runner-at-any-scale

**Running container for dev**
```bash
docker run -d --name todo_cont1 -p 8000:8000 simple_todo 
```

**Check the Browser**

    http://localhost:8000/docs

**Test the container**
```bash
docker run -it --rm simple_todo /bin/bash -c "poetry run pytest"
```
**List Running Containers**
```bash
docker ps
```

**List all contaieners**
```bash
docker ps -a
```

**Interect with the container**

```bash
docker exec -it dev_cont1 /bin/bash
```

**Exit from the shell**
```bash
exit
```

**Stop the running container**

`dev_cont1` is the name of container which is running

```bash
docker stop dev_cont1
```

**Remove the container**
```bash
docker rm dev_cont1
```

**Run the container in background**

    CTRL + P + Q

Write the first 4 words of id to run container with id

```bash
docker exec -it 4e3f /bin/bash
```

```bash
docker exec -it dev_cont1 /bin/bash
```

**Create  imaege from running container**

```bash
docker commit af4e imagefromcontainer
```











8