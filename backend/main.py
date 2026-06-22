"""
Main FastAPI application for SmartReview
Entry point for the API server
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import trades, stats, accounts, ai_coach

# Initialize FastAPI app
app = FastAPI(
    title="SmartReview API",
    description="Intelligent Trading Journal with AI Integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"status": "SmartReview API running", "version": "1.0.0"}


# Include routers
app.include_router(trades.router, prefix="/api/trades", tags=["trades"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(ai_coach.router, prefix="/api/ai", tags=["ai-coach"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all uncaught exceptions"""
    raise HTTPException(status_code=500, detail=str(exc))


# Startup event - initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
