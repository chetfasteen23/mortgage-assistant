from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.uploads import router as uploads_router
from app.api.search import router as search_router

app = FastAPI(title="Mortgage Assistant API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(uploads_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {"message": "Mortgage Assistant API is running"}