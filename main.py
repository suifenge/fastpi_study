from fastapi import FastAPI
from routers.user import usersRouter
from models.redis_cache import get_redis
import uvicorn

app = FastAPI()
app.include_router(usersRouter, prefix="/user", tags=["users"])


@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis()


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)
