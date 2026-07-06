from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services.router import router
app = FastAPI(
    title="Customer Journey AI",
    version="1.0"
)

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Customer Journey AI Backend Running"
    }