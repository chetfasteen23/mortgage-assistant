from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Mortgage Assistant API is running"}