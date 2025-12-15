from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, post, auth, votes
from . import models
from .database import engine
from .config import settings
app = FastAPI()

#models.Base.metadata.create_all(bind=engine)
# we don't need this code because we are using alembic
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)