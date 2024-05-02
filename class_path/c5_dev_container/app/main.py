from fastapi import FastAPI

app : FastAPI = FastAPI( title="Class 05 Practice" )

app.get("/")
async def root():
    return {"message": "Welcome to Class 05 Practice"}