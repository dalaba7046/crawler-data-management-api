from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.item_api import router as item_router
from app.routers.mongo_api import router as mongo_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"message": "Hello World"}

# 包含不同功能的 API 文件路由
app.include_router(item_router, prefix="/v1/item", tags=["jd_item"])
app.include_router(mongo_router, prefix="/v1/mongo", tags=["mongo_raw_data"])



