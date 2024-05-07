from fastapi import FastAPI

app : FastAPI = FastAPI(
    title="practice project",
)


@app.get("/")
async def root():
    return {"message": "Class 05 & 06 practice code"}

@app.get("/aqeel")
async def get_admin():
    return {"Admin" :"class practice"}