"""
Pydantic schemas for request/response validation
Defines the data structures for API endpoints
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Account schemas
class AccountBase(BaseModel):
    name: str = Field(..., max_length=100)
    broker: Optional[str] = Field(None, max_length=100)
    type: str = Field(..., description="PERSONAL or PROP_FIRM")
    prop_firm_name: Optional[str] = Field(None, max_length=100)
    initial_balance: float = 0.0
    current_balance: float = 0.0
    daily_drawdown_limit: Optional[float] = None
    max_drawdown_limit: Optional[float] = None
    profit_target: Optional[float] = None
    challenge_phase: Optional[str] = Field(None, max_length=50)
    is_active: bool = True


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    broker: Optional[str] = None
    current_balance: Optional[float] = None
    daily_drawdown_limit: Optional[float] = None
    max_drawdown_limit: Optional[float] = None
    profit_target: Optional[float] = None
    challenge_phase: Optional[str] = None
    is_active: Optional[bool] = None


class Account(AccountBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Trade schemas
class TradeBase(BaseModel):
    account_id: int
    asset: str = Field(..., max_length=20)
    direction: str = Field(..., description="BUY or SELL")
    entry_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    exit_price: Optional[float] = None
    lot_size: float
    risk_amount: Optional[float] = None
    rr_planned: Optional[float] = None
    rr_obtained: Optional[float] = None
    result: Optional[str] = Field(None, description="WIN, LOSS, BREAKEVEN")
    profit_loss: float = 0.0
    setup: Optional[str] = Field(None, max_length=100)
    market_structure: Optional[str] = Field(None, max_length=50)
    market_context: Optional[str] = Field(None, max_length=100)
    liquidity_targeted: Optional[str] = Field(None, max_length=50)
    reasoning: Optional[str] = None
    confidence_level: Optional[int] = Field(None, ge=1, le=10)
    emotional_state: Optional[str] = Field(None, max_length=50)
    discipline_felt: Optional[str] = Field(None, max_length=50)
    plan_respected: bool = True
    session: Optional[str] = Field(None, description="ASIA, LONDON, NEW_YORK")
    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None
    trade_date: Optional[datetime] = None
    screenshot_before: Optional[str] = Field(None, max_length=500)
    screenshot_after: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = None


class TradeCreate(TradeBase):
    pass


class TradeUpdate(BaseModel):
    asset: Optional[str] = None
    direction: Optional[str] = None
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    exit_price: Optional[float] = None
    lot_size: Optional[float] = None
    risk_amount: Optional[float] = None
    rr_planned: Optional[float] = None
    rr_obtained: Optional[float] = None
    result: Optional[str] = None
    profit_loss: Optional[float] = None
    setup: Optional[str] = None
    market_structure: Optional[str] = None
    market_context: Optional[str] = None
    liquidity_targeted: Optional[str] = None
    reasoning: Optional[str] = None
    confidence_level: Optional[int] = Field(None, ge=1, le=10)
    emotional_state: Optional[str] = None
    discipline_felt: Optional[str] = None
    plan_respected: Optional[bool] = None
    session: Optional[str] = None
    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None
    screenshot_before: Optional[str] = None
    screenshot_after: Optional[str] = None
    notes: Optional[str] = None


class Trade(TradeBase):
    id: int
    trading_score: int
    created_at: datetime

    class Config:
        from_attributes = True


# Stats schemas
class StatsResponse(BaseModel):
    total_trades: int
    win_rate: float
    profit_factor: float
    average_rr: float
    expectancy: float
    max_drawdown: float
    current_drawdown: float
    total_profit: float
    total_loss: float
    net_profit: float
    average_trading_score: float
    plan_respect_rate: float


# AI Coach schemas
class AIAnalysisRequest(BaseModel):
    account_id: int
    period: Optional[str] = "30d"  # 7d, 30d, 90d, all


class AIAnalysisResponse(BaseModel):
    insights: list
    recommendations: list
    strengths: list
    weaknesses: list
    overall_score: int
