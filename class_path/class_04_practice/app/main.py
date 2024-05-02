from fastapi import FastAPI

app : FastAPI = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to onsite class 04 code"}