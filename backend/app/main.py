"""
Application principale FastAPI - Job Hunter AI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db, close_db


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
from app.api import auth, profile, job_offer, analysis, documents
from app.api.routes import search, company_watch, custom_sources, contact
from app.api.v1.endpoints import applications

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(profile.router, prefix="/api/v1", tags=["Profile"])
app.include_router(job_offer.router)
app.include_router(analysis.router)
app.include_router(documents.router)
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(company_watch.router, prefix="/api/v1", tags=["Company Watch"])
app.include_router(custom_sources.router, prefix="/api/v1", tags=["Custom Sources"])
app.include_router(applications.router, prefix="/api/v1/applications", tags=["Applications"])
app.include_router(contact.router, prefix="/api/v1/contact", tags=["Contact"])
