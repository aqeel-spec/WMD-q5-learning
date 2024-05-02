

1. create new project using

```cmd
    poetry new backend
```

2. Go into working directory

```cmd
cd backend
```

3. Install `sqlmodel` and `uvicorn[standard]`

```cmd
poetry add fastapi sqlmodel "uvicorn[standard]"
```

4. Now install the dependencies of `pyproject.toml` and create `virtual environment`

```cmd
poetry install
```

5. Follow the following steps to remove imports errors
    * Activate `Virtual env` 
        ```shell
        poetry shell
        ```
    * In my case 
    ```shell
        (backend-py3.11) D:\WMD-q5-learning\my_learning\todo_with_poetry_dockerize\backend>poetry shell
        Creating virtualenv backend-r4GJ9vLm-py3.11 in C:\Users\PC\AppData\Local\pypoetry\Cache\virtualenvs
        Virtual environment already activated: C:\Users\PC\AppData\Local\pypoetry\Cache\virtualenvs\backend-r4GJ9vLm-py3.11
    ```
    * Copy the env path `C:\Users\PC\AppData\Local\pypoetry\Cache\virtualenvs\backend-r4GJ9vLm-py3.11`
    * In vscode press `Ctrl + Shift + p` 
        * Select `Python select interpreter`
        * Then select `Enter interpreter path...`
        * Enter the path and hit enter `C:\Users\PC\AppData\Local\pypoetry\Cache\virtualenvs\backend-r4GJ9vLm-py3.11`

5. Create main.py file and add the following code

```python
from fastapi import FastAPI

app : FastAPI = FastAPI()

@app.get("/")
def root():
    return {"Hello": "world"}
```

6. Run the unicorn server
```terminal
poetry run uvicorn heroapi_uit.main:app --reload
```