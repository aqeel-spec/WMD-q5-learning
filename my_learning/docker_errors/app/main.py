from fastapi import FastAPI

app : FastAPI = FastAPI(
    title="Docker errors handle with fastapi",
)


@app.get("/")
async def root():
    return {"message": "Docker Error handling is running!"}

@app.get("/aqeel")
async def definer():
    return {
        "name" : "Aqeel Shahzad",
        "email" : "aqeelshahzad1215@gmail.com",
        "ph" : "03471756159"
    }
    
@app.post("/login")
async def user_Access():
    return {
        "message" : "Login successful"
    }

