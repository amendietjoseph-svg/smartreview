"""
Main FastAPI application for SmartFX-Review
"""
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import init_db
from routers import trades, stats, accounts, ai_coach, auth, import_trades

app = FastAPI(
    title="SmartFX-Review API",
    description="Intelligent Trading Journal with AI Integration",
    version="1.0.0"
)

# CORS - Must be first middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "SmartFX-Review API running", "version": "1.0.0"}

# Include routers - no trailing slash issues
app.include_router(trades.router, prefix="/api/trades", tags=["trades"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(ai_coach.router, prefix="/api/ai", tags=["ai-coach"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(import_trades.router, prefix="/api/import", tags=["import"])

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Not Found", "path": str(request.url)},
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.on_event("startup")
async def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
