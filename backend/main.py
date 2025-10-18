from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from common.settings import settings
from common.database import db
from api import auth, chats, messages, ai_config

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered customer messaging management system",
    version="1.0.0",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(messages.router)
app.include_router(ai_config.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await db.init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    await db.close_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Customer Messaging System API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    if settings.debug:
        raise exc
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )