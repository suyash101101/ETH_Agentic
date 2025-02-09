from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from .api.zk_files_routes.routes import router as zk_files_router
from .api.web3_routes.routes import router as web3_router

app = FastAPI()  # Adjust path as needed

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent manager at startup
app.include_router(zk_files_router, prefix="/zkproof", tags=["zkproof"])
app.include_router(web3_router, prefix="/api", tags=["web3"])