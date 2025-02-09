from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from .api.zk_files_routes.routes import router as zk_files_router

app = FastAPI()  # Adjust path as needed

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(zk_files_router, prefix="/zkproof", tags=["zkproof"])