from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from common.settings import settings
from common.database import db
from api import auth, chats, messages, ai_config
from models import User, Company
from fastapi import FastAPI

from fastadmin import fastapi_app as admin_app
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    await db.init_db()

    # Create superadmin user if not exists
    from services.auth_service import auth_service

    existing_admin = await db.get_record_by_field(User, email=settings.superadmin_email)
    if not existing_admin:
        # Create a default company for the superadmin
        admin_company = await db.create_record(Company, name="Admin Company")

        # Create superadmin user
        password_hash = auth_service.get_password_hash(settings.superadmin_password)
        await db.create_record(
            User,
            email=settings.superadmin_email,
            password_hash=password_hash,
            name="Super Admin",
            company_id=admin_company.id,
            is_superuser=True,
            is_active=True,
        )

    yield

    # Shutdown
    await db.close_db()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered customer messaging management system",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# Add CORS middleware - allow both local and ngrok origins
cors_origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:8001",
    "https://profound-normally-crappie.ngrok-free.app",
    "https://8525c1343c5f.ngrok-free.app",
    # Allow all ngrok domains
    "https://*.ngrok-free.app",
    # Add any other ngrok URLs you might use
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "ngrok-skip-browser-warning",
        "Ngrok-Skip-Browser-Warning",
    ],
)

# Include routers
app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(messages.router)
app.include_router(ai_config.router)
app.mount("/admin", admin_app)


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

    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
