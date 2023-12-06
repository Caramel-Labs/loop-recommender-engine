from fastapi import FastAPI
from routes.router import router

# instantiate FastAPI app
app = FastAPI()

# setup router
app.include_router(router)
