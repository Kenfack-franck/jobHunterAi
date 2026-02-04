"""
Application principale FastAPI - Job Hunter AI
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import init_db, close_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestion du cycle de vie de l'application
    """
    # Startup
    print("🚀 Démarrage de Job Hunter AI...")
    # Note: En production, utiliser Alembic plutôt que init_db()
    # await init_db()
    print("✅ Base de données connectée")
    
    yield
    
    # Shutdown
    print("🔌 Fermeture des connexions...")
    await close_db()
    print("✅ Application arrêtée proprement")


# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API REST pour automatiser la recherche d'emploi et générer des candidatures personnalisées",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Handler pour les erreurs de validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler pour afficher les détails des erreurs de validation"""
    try:
        body = await request.body()
        body_str = body.decode('utf-8')[:1000] if body else "N/A"
    except:
        body_str = "Unable to decode body"
    
    logger.error(f"❌ Validation error on {request.method} {request.url}")
    logger.error(f"Body (first 1000 chars): {body_str}")
    logger.error(f"Validation errors: {exc.errors()}")
    
    # Convert Pydantic errors to JSON-serializable format
    errors = []
    for error in exc.errors():
        error_dict = dict(error)
        # Convert any bytes to string
        if 'input' in error_dict and isinstance(error_dict['input'], bytes):
            error_dict['input'] = error_dict['input'].decode('utf-8', errors='ignore')
        errors.append(error_dict)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": errors
        }
    )


# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes de base
@app.get("/")
async def root():
    """Route de base"""
    return {
        "message": "🎯 Job Hunter AI API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check pour le monitoring"""
    return {
        "status": "healthy",
        "version": settings.VERSION
    }


# Importer et enregistrer les routes
from app.api import auth, profile, job_offer, analysis, documents, sources
from app.api.routes import search, company_watch, custom_sources, contact, admin
from app.api.v1.endpoints import applications

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(profile.router, prefix="/api/v1", tags=["Profile"])
app.include_router(job_offer.router)
app.include_router(analysis.router)
app.include_router(documents.router)
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(sources.router, prefix="/api/v1/sources", tags=["Sources"])
app.include_router(company_watch.router, prefix="/api/v1", tags=["Company Watch"])
app.include_router(custom_sources.router, prefix="/api/v1", tags=["Custom Sources"])
app.include_router(applications.router, prefix="/api/v1/applications", tags=["Applications"])
app.include_router(contact.router, prefix="/api/v1/contact", tags=["Contact"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])
