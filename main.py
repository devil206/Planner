from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router
import uvicorn

app = FastAPI()

# Register routes

app.include_router(user_router,  prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def home():
    return {"message":"Welcome to the MongoDB version"}

if __name__ == '__main__':
    uvicorn.run("main:app", host= "0.0.0.0", port = 8000, log_level= "info", reload=True)

