"""
Router for AI Coach operations
Endpoints for AI-powered trading analysis and recommendations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import Trade, Account, AIAnalysis
from pydantic import BaseModel
from typing import Optional
from services.ai_service import AIService

router = APIRouter()


class AnalyzeRequest(BaseModel):
    account_id: int
    period: str = "30d"


class EdgeRequest(BaseModel):
    account_id: int


class DailyReportRequest(BaseModel):
    account_id: int


class WeeklyReportRequest(BaseModel):
    account_id: int


@router.post("/analyze")
async def analyze_trading_performance(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze trading performance using Claude AI
    Returns comprehensive markdown analysis
    """
    # Get account
    account = db.query(Account).filter(Account.id == request.account_id).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Get trades for the account
    trades = db.query(Trade).filter(Trade.account_id == request.account_id).all()
    
    if not trades:
        return {"analysis": "# Aucune donnée disponible\n\nCommencez à enregistrer vos trades pour obtenir une analyse personnalisée."}
    
    # Check for cached analysis (6h cache)
    cache_cutoff = datetime.now() - timedelta(hours=6)
    cached_analysis = db.query(AIAnalysis).filter(
        AIAnalysis.account_id == request.account_id,
        AIAnalysis.analysis_type == "performance",
        AIAnalysis.period == request.period,
        AIAnalysis.created_at >= cache_cutoff
    ).first()
    
    if cached_analysis:
        return {"analysis": cached_analysis.content, "cached": True}
    
    # Use AI service to analyze
    ai_service = AIService()
    analysis = await ai_service.analyze_performance(trades, account, request.period)
    
    # Save analysis to database
    new_analysis = AIAnalysis(
        account_id=request.account_id,
        analysis_type="performance",
        period=request.period,
        content=analysis,
        created_at=datetime.now()
    )
    db.add(new_analysis)
    db.commit()
    
    return {"analysis": analysis, "cached": False}


@router.post("/edge")
async def detect_edge(
    request: EdgeRequest,
    db: Session = Depends(get_db)
):
    """
    Detect statistical edges by crossing all variables
    Returns top 5 edges with composite scores
    """
    # Get trades for the account
    trades = db.query(Trade).filter(Trade.account_id == request.account_id).all()
    
    if not trades:
        return {"edges": []}
    
    # Use AI service to detect edges
    ai_service = AIService()
    edges = ai_service.detect_edge(trades)
    
    return {"edges": edges}


@router.post("/daily-report")
async def generate_daily_report(
    request: DailyReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generate daily report comparing today's performance to historical average
    """
    # Get trades for the account
    all_trades = db.query(Trade).filter(Trade.account_id == request.account_id).all()
    
    if not all_trades:
        return {"report": "# Rapport du Jour\n\nAucun trade effectué aujourd'hui."}
    
    # Get today's trades
    today = datetime.now().date()
    trades_today = [t for t in all_trades if t.trade_date and datetime.fromisoformat(t.trade_date.replace('Z', '+00:00')).date() == today]
    
    # Get historical trades (last 30 days excluding today)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    historical_trades = [
        t for t in all_trades 
        if t.trade_date and datetime.fromisoformat(t.trade_date.replace('Z', '+00:00')) >= thirty_days_ago
        and not (t.trade_date and datetime.fromisoformat(t.trade_date.replace('Z', '+00:00')).date() == today)
    ]
    
    # Use AI service to generate report
    ai_service = AIService()
    report = await ai_service.generate_daily_report(trades_today, historical_trades)
    
    return {"report": report}


@router.post("/weekly-summary")
async def generate_weekly_summary(
    request: WeeklyReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generate weekly summary with trends and advice
    """
    # Get trades for the account
    all_trades = db.query(Trade).filter(Trade.account_id == request.account_id).all()
    
    if not all_trades:
        return {"summary": "# Résumé Hebdomadaire\n\nAucun trade cette semaine."}
    
    # Get this week's trades
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    trades_week = [
        t for t in all_trades 
        if t.trade_date and datetime.fromisoformat(t.trade_date.replace('Z', '+00:00')) >= week_start
    ]
    
    # Use AI service to generate summary
    ai_service = AIService()
    summary = await ai_service.generate_weekly_summary(trades_week)
    
    return {"summary": summary}


@router.get("/insights/{account_id}")
def get_insights(account_id: int, db: Session = Depends(get_db)):
    """
    Get the last saved analyses for an account
    Returns analysis history with timestamps
    """
    analyses = db.query(AIAnalysis).filter(
        AIAnalysis.account_id == account_id
    ).order_by(AIAnalysis.created_at.desc()).limit(10).all()
    
    return {
        "insights": [
            {
                "id": a.id,
                "type": a.analysis_type,
                "period": a.period,
                "content": a.content,
                "created_at": a.created_at.isoformat()
            }
            for a in analyses
        ]
    }


@router.get("/edge/{account_id}")
def get_edge_tracker(account_id: int, db: Session = Depends(get_db)):
    """
    Get edge tracker data
    Shows which setups, sessions, and assets have the highest edge
    """
    trades = db.query(Trade).filter(Trade.account_id == account_id).all()
    
    if not trades:
        return {
            "best_setups": [],
            "best_sessions": [],
            "best_assets": [],
            "worst_setups": [],
            "worst_sessions": [],
            "worst_assets": []
        }
    
    # Analyze by setup
    setup_stats = {}
    for trade in trades:
        if trade.setup:
            if trade.setup not in setup_stats:
                setup_stats[trade.setup] = {
                    "wins": 0,
                    "total": 0,
                    "profit": 0.0,
                    "avg_rr": 0.0,
                    "total_rr": 0.0
                }
            setup_stats[trade.setup]["total"] += 1
            setup_stats[trade.setup]["profit"] += trade.profit_loss
            if trade.rr_obtained:
                setup_stats[trade.setup]["total_rr"] += trade.rr_obtained
            if trade.result == "WIN":
                setup_stats[trade.setup]["wins"] += 1
    
    # Calculate metrics for setups
    for setup in setup_stats:
        setup_stats[setup]["win_rate"] = (
            setup_stats[setup]["wins"] / setup_stats[setup]["total"] * 100
            if setup_stats[setup]["total"] > 0 else 0
        )
        setup_stats[setup]["avg_rr"] = (
            setup_stats[setup]["total_rr"] / setup_stats[setup]["total"]
            if setup_stats[setup]["total"] > 0 else 0
        )
    
    # Sort and get best/worst
    sorted_setups = sorted(
        setup_stats.items(),
        key=lambda x: (x[1]["win_rate"], x[1]["profit"]),
        reverse=True
    )
    
    best_setups = [
        {"name": s[0], **s[1]}
        for s in sorted_setups[:5]
    ]
    worst_setups = [
        {"name": s[0], **s[1]}
        for s in sorted_setups[-5:]
    ]
    
    # Similar analysis for sessions and assets
    session_stats = {}
    for trade in trades:
        if trade.session:
            if trade.session not in session_stats:
                session_stats[trade.session] = {"wins": 0, "total": 0, "profit": 0.0}
            session_stats[trade.session]["total"] += 1
            session_stats[trade.session]["profit"] += trade.profit_loss
            if trade.result == "WIN":
                session_stats[trade.session]["wins"] += 1
    
    for session in session_stats:
        session_stats[session]["win_rate"] = (
            session_stats[session]["wins"] / session_stats[session]["total"] * 100
            if session_stats[session]["total"] > 0 else 0
        )
    
    sorted_sessions = sorted(
        session_stats.items(),
        key=lambda x: (x[1]["win_rate"], x[1]["profit"]),
        reverse=True
    )
    
    best_sessions = [
        {"name": s[0], **s[1]}
        for s in sorted_sessions[:3]
    ]
    worst_sessions = [
        {"name": s[0], **s[1]}
        for s in sorted_sessions[-3:]
    ]
    
    asset_stats = {}
    for trade in trades:
        if trade.asset not in asset_stats:
            asset_stats[trade.asset] = {"wins": 0, "total": 0, "profit": 0.0}
        asset_stats[trade.asset]["total"] += 1
        asset_stats[trade.asset]["profit"] += trade.profit_loss
        if trade.result == "WIN":
            asset_stats[trade.asset]["wins"] += 1
    
    for asset in asset_stats:
        asset_stats[asset]["win_rate"] = (
            asset_stats[asset]["wins"] / asset_stats[asset]["total"] * 100
            if asset_stats[asset]["total"] > 0 else 0
        )
    
    sorted_assets = sorted(
        asset_stats.items(),
        key=lambda x: (x[1]["win_rate"], x[1]["profit"]),
        reverse=True
    )
    
    best_assets = [
        {"name": a[0], **a[1]}
        for a in sorted_assets[:5]
    ]
    worst_assets = [
        {"name": a[0], **a[1]}
        for a in sorted_assets[-5:]
    ]
    
    return {
        "best_setups": best_setups,
        "best_sessions": best_sessions,
        "best_assets": best_assets,
        "worst_setups": worst_setups,
        "worst_sessions": worst_sessions,
        "worst_assets": worst_assets
    }
