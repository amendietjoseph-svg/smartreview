"""
Router for statistics operations
Endpoints for calculating and retrieving trading statistics
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from models import Trade
from schemas import StatsResponse
from services.stats_calculator import StatsCalculator

router = APIRouter()


@router.get("/account/{account_id}", response_model=StatsResponse)
def get_account_stats(
    account_id: int,
    period: str = "all",  # 7d, 30d, 90d, all
    db: Session = Depends(get_db)
):
    """
    Get statistics for a specific account
    Period can be: 7d, 30d, 90d, all
    """
    # Calculate date filter based on period
    date_filter = None
    if period == "7d":
        date_filter = datetime.utcnow() - timedelta(days=7)
    elif period == "30d":
        date_filter = datetime.utcnow() - timedelta(days=30)
    elif period == "90d":
        date_filter = datetime.utcnow() - timedelta(days=90)
    
    # Query trades
    query = db.query(Trade).filter(Trade.account_id == account_id)
    
    if date_filter:
        query = query.filter(Trade.trade_date >= date_filter)
    
    trades = query.all()
    
    if not trades:
        # Return empty stats if no trades
        return StatsResponse(
            total_trades=0,
            win_rate=0.0,
            profit_factor=0.0,
            average_rr=0.0,
            expectancy=0.0,
            max_drawdown=0.0,
            current_drawdown=0.0,
            total_profit=0.0,
            total_loss=0.0,
            net_profit=0.0,
            average_trading_score=0.0,
            plan_respect_rate=0.0
        )
    
    # Calculate stats
    calculator = StatsCalculator()
    stats = calculator.calculate_all_stats(trades)
    
    return StatsResponse(**stats)


@router.get("/equity/{account_id}")
def get_equity_curve(
    account_id: int,
    period: str = "all",
    db: Session = Depends(get_db)
):
    """
    Get equity curve data for charting
    Returns array of {date, balance} points
    """
    # Calculate date filter
    date_filter = None
    if period == "7d":
        date_filter = datetime.utcnow() - timedelta(days=7)
    elif period == "30d":
        date_filter = datetime.utcnow() - timedelta(days=30)
    elif period == "90d":
        date_filter = datetime.utcnow() - timedelta(days=90)
    
    # Query trades ordered by date
    query = db.query(Trade).filter(Trade.account_id == account_id)
    
    if date_filter:
        query = query.filter(Trade.trade_date >= date_filter)
    
    trades = query.order_by(Trade.trade_date.asc()).all()
    
    # Build equity curve
    equity_curve = []
    running_balance = 0.0
    
    for trade in trades:
        running_balance += trade.profit_loss
        equity_curve.append({
            "date": trade.trade_date.isoformat(),
            "balance": running_balance,
            "trade_id": trade.id
        })
    
    return {"equity_curve": equity_curve}


@router.get("/performance/{account_id}")
def get_performance_metrics(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed performance metrics including:
    - Win rate by session
    - Win rate by asset
    - Average RR by setup
    """
    trades = db.query(Trade).filter(Trade.account_id == account_id).all()
    
    if not trades:
        return {
            "by_session": {},
            "by_asset": {},
            "by_setup": {}
        }
    
    # Calculate by session
    by_session = {}
    for trade in trades:
        if trade.session:
            if trade.session not in by_session:
                by_session[trade.session] = {"wins": 0, "total": 0}
            by_session[trade.session]["total"] += 1
            if trade.result == "WIN":
                by_session[trade.session]["wins"] += 1
    
    # Calculate win rates
    for session in by_session:
        by_session[session]["win_rate"] = (
            by_session[session]["wins"] / by_session[session]["total"] * 100
            if by_session[session]["total"] > 0 else 0
        )
    
    # Calculate by asset
    by_asset = {}
    for trade in trades:
        if trade.asset not in by_asset:
            by_asset[trade.asset] = {"wins": 0, "total": 0, "profit": 0.0}
        by_asset[trade.asset]["total"] += 1
        by_asset[trade.asset]["profit"] += trade.profit_loss
        if trade.result == "WIN":
            by_asset[trade.asset]["wins"] += 1
    
    for asset in by_asset:
        by_asset[asset]["win_rate"] = (
            by_asset[asset]["wins"] / by_asset[asset]["total"] * 100
            if by_asset[asset]["total"] > 0 else 0
        )
    
    # Calculate by setup
    by_setup = {}
    for trade in trades:
        if trade.setup:
            if trade.setup not in by_setup:
                by_setup[trade.setup] = {"wins": 0, "total": 0, "avg_rr": 0.0, "total_rr": 0.0}
            by_setup[trade.setup]["total"] += 1
            if trade.rr_obtained:
                by_setup[trade.setup]["total_rr"] += trade.rr_obtained
            if trade.result == "WIN":
                by_setup[trade.setup]["wins"] += 1
    
    for setup in by_setup:
        by_setup[setup]["win_rate"] = (
            by_setup[setup]["wins"] / by_setup[setup]["total"] * 100
            if by_setup[setup]["total"] > 0 else 0
        )
        by_setup[setup]["avg_rr"] = (
            by_setup[setup]["total_rr"] / by_setup[setup]["total"]
            if by_setup[setup]["total"] > 0 else 0
        )
    
    return {
        "by_session": by_session,
        "by_asset": by_asset,
        "by_setup": by_setup
    }
