"""
Router for trade operations
CRUD endpoints for managing trades
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Trade
from schemas import TradeCreate, TradeUpdate, Trade as TradeSchema
from services.stats_calculator import StatsCalculator

router = APIRouter()


@router.post("/", response_model=TradeSchema)
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    """
    Create a new trade
    Automatically calculates trading score based on discipline metrics
    """
    # Calculate trading score
    calculator = StatsCalculator()
    trading_score = calculator.calculate_trading_score(trade)
    
    # Create trade object
    db_trade = Trade(**trade.dict(), trading_score=trading_score)
    
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    
    return db_trade


@router.get("/", response_model=List[TradeSchema])
def get_trades(
    skip: int = 0,
    limit: int = 100,
    account_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Get all trades with optional filtering
    """
    query = db.query(Trade)
    
    if account_id:
        query = query.filter(Trade.account_id == account_id)
    
    trades = query.order_by(Trade.trade_date.desc()).offset(skip).limit(limit).all()
    return trades


@router.get("/{trade_id}", response_model=TradeSchema)
def get_trade(trade_id: int, db: Session = Depends(get_db)):
    """
    Get a specific trade by ID
    """
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    return trade


@router.put("/{trade_id}", response_model=TradeSchema)
def update_trade(
    trade_id: int,
    trade_update: TradeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing trade
    Recalculates trading score if relevant fields are updated
    """
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()
    
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    # Update fields
    update_data = trade_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_trade, field, value)
    
    # Recalculate trading score if relevant fields changed
    score_fields = ['plan_respected', 'confidence_level', 'discipline_felt', 'rr_obtained', 'rr_planned']
    if any(field in update_data for field in score_fields):
        calculator = StatsCalculator()
        db_trade.trading_score = calculator.calculate_trading_score(db_trade)
    
    db.commit()
    db.refresh(db_trade)
    
    return db_trade


@router.delete("/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    """
    Delete a trade
    """
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()
    
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    db.delete(db_trade)
    db.commit()
    
    return {"message": "Trade deleted successfully"}
