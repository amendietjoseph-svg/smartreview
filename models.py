"""
SQLAlchemy models for SmartReview database
Defines the structure of Trades and Accounts tables
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Account(Base):
    """
    Trading account model
    Supports both personal accounts and prop firm challenges
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    broker = Column(String(100))
    type = Column(String(20), nullable=False)  # PERSONAL or PROP_FIRM
    prop_firm_name = Column(String(100), nullable=True)
    initial_balance = Column(Float, default=0.0)
    current_balance = Column(Float, default=0.0)
    daily_drawdown_limit = Column(Float, nullable=True)
    max_drawdown_limit = Column(Float, nullable=True)
    profit_target = Column(Float, nullable=True)
    challenge_phase = Column(String(50), nullable=True)  # Phase 1, Phase 2, Funded, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with trades
    trades = relationship("Trade", back_populates="account", cascade="all, delete-orphan")


class Trade(Base):
    """
    Trade model with comprehensive tracking
    Includes entry/exit details, risk management, and psychology metrics
    """
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    
    # Trade basics
    asset = Column(String(20), nullable=False)  # e.g., EURUSD, BTCUSD
    direction = Column(String(10), nullable=False)  # BUY or SELL
    entry_price = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)
    
    # Position sizing
    lot_size = Column(Float, nullable=False)
    risk_amount = Column(Float, nullable=True)
    rr_planned = Column(Float, nullable=True)  # Risk:Reward ratio planned
    rr_obtained = Column(Float, nullable=True)  # Risk:Reward ratio obtained
    
    # Results
    result = Column(String(20), nullable=True)  # WIN, LOSS, BREAKEVEN
    profit_loss = Column(Float, default=0.0)
    
    # Trading setup and context
    setup = Column(String(100), nullable=True)  # e.g., MSS+Sweep, Break of Structure
    market_structure = Column(String(50), nullable=True)
    market_context = Column(String(100), nullable=True)
    liquidity_targeted = Column(String(50), nullable=True)
    reasoning = Column(Text, nullable=True)
    
    # Psychology and discipline
    confidence_level = Column(Integer, nullable=True)  # 1-10
    emotional_state = Column(String(50), nullable=True)
    discipline_felt = Column(String(50), nullable=True)
    plan_respected = Column(Boolean, default=True)
    
    # Session information
    session = Column(String(20), nullable=True)  # ASIA, LONDON, NEW_YORK
    
    # Timing
    entry_time = Column(DateTime, nullable=True)
    exit_time = Column(DateTime, nullable=True)
    trade_date = Column(DateTime, default=datetime.utcnow)
    
    # Screenshots and notes
    screenshot_before = Column(String(500), nullable=True)  # URL or path
    screenshot_after = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Calculated score
    trading_score = Column(Integer, default=0)  # 0-100
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with account
    account = relationship("Account", back_populates="trades")


class AIAnalysis(Base):
    """
    AI Analysis model for storing Claude API analyses
    Stores performance analyses, edge detection, and reports
    """
    __tablename__ = "ai_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    analysis_type = Column(String)  # "performance", "edge", "daily", "weekly"
    content = Column(Text)
    period = Column(String, nullable=True)
    trades_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
