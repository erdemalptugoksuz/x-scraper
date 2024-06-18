from fastapi import FastAPI
from controllers import user_profile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user_profile.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
