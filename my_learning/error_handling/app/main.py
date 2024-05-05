from fastapi import FastAPI

app : FastAPI = FastAPI()

@app.get("/")
def main():
    return {"message": "Error handling with fastapi and docker"}