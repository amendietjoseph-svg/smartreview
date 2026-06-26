"""
MT5/MT4 Trade Import Router
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Trade
import csv
import io
from datetime import datetime

router = APIRouter()

def parse_mt5_csv(content: str, account_id: int):
    """Parse MT5 history export CSV"""
    trades = []
    lines = content.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("Time"):
            continue
        
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 10:
            continue
            
        try:
            # MT5 format: #,Time,Deal,Symbol,Type,Direction,Volume,Price,Order,Commission,Swap,Profit,Balance
            trade_type = parts[4].lower() if len(parts) > 4 else ""
            direction = parts[5].lower() if len(parts) > 5 else ""
            
            if direction not in ["in", "out"] and trade_type not in ["buy", "sell"]:
                continue
                
            if direction == "out" or (trade_type in ["buy", "sell"] and direction == "out"):
                profit = float(parts[11]) if len(parts) > 11 else 0
                volume = float(parts[6]) if len(parts) > 6 else 0
                price = float(parts[7]) if len(parts) > 7 else 0
                symbol = parts[3] if len(parts) > 3 else ""
                commission = float(parts[9]) if len(parts) > 9 else 0
                swap = float(parts[10]) if len(parts) > 10 else 0
                
                time_str = parts[1] if len(parts) > 1 else ""
                try:
                    trade_time = datetime.strptime(time_str, "%Y.%m.%d %H:%M:%S")
                except:
                    try:
                        trade_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    except:
                        trade_time = datetime.now()
                
                trade = {
                    "account_id": account_id,
                    "asset": symbol,
                    "direction": "BUY" if trade_type == "buy" else "SELL",
                    "entry_price": price,
                    "exit_price": price,
                    "lot_size": volume,
                    "profit_loss": profit,
                    "result": "WIN" if profit > 0 else "LOSS" if profit < 0 else "BREAKEVEN",
                    "trade_date": trade_time.strftime("%Y-%m-%d"),
                    "entry_time": trade_time.strftime("%H:%M:%S"),
                    "risk_amount": abs(commission),
                    "notes": f"Import MT5 | Commission: {commission} | Swap: {swap}"
                }
                trades.append(trade)
        except Exception as e:
            continue
    
    return trades

def parse_mt4_csv(content: str, account_id: int):
    """Parse MT4 history export CSV"""
    trades = []
    lines = content.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if not line or "#" in line[:5] or "Ticket" in line:
            continue
            
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 10:
            continue
            
        try:
            # MT4 format: Ticket,Open Time,Type,Size,Item,Price,S/L,T/P,Close Time,Close Price,Commission,Swap,Profit
            ticket = parts[0]
            open_time_str = parts[1] if len(parts) > 1 else ""
            trade_type = parts[2].lower() if len(parts) > 2 else ""
            size = float(parts[3]) if len(parts) > 3 else 0
            symbol = parts[4] if len(parts) > 4 else ""
            open_price = float(parts[5]) if len(parts) > 5 else 0
            sl = float(parts[6]) if len(parts) > 6 and parts[6] else 0
            tp = float(parts[7]) if len(parts) > 7 and parts[7] else 0
            close_price = float(parts[9]) if len(parts) > 9 else 0
            commission = float(parts[10]) if len(parts) > 10 else 0
            swap = float(parts[11]) if len(parts) > 11 else 0
            profit = float(parts[12]) if len(parts) > 12 else 0
            
            if trade_type not in ["buy", "sell"]:
                continue
            
            try:
                trade_time = datetime.strptime(open_time_str, "%Y.%m.%d %H:%M:%S")
            except:
                try:
                    trade_time = datetime.strptime(open_time_str, "%Y-%m-%d %H:%M:%S")
                except:
                    trade_time = datetime.now()
            
            trade = {
                "account_id": account_id,
                "asset": symbol,
                "direction": "BUY" if trade_type == "buy" else "SELL",
                "entry_price": open_price,
                "exit_price": close_price,
                "stop_loss": sl if sl > 0 else None,
                "take_profit": tp if tp > 0 else None,
                "lot_size": size,
                "profit_loss": profit,
                "result": "WIN" if profit > 0 else "LOSS" if profit < 0 else "BREAKEVEN",
                "trade_date": trade_time.strftime("%Y-%m-%d"),
                "entry_time": trade_time.strftime("%H:%M:%S"),
                "notes": f"Import MT4 | Ticket: {ticket} | Commission: {commission} | Swap: {swap}"
            }
            trades.append(trade)
        except Exception as e:
            continue
    
    return trades

@router.post("/mt5")
async def import_mt5(
    file: UploadFile = File(...),
    account_id: int = 1,
    db: Session = Depends(get_db)
):
    """Import trades from MT5 CSV export"""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    
    # Auto-detect MT4 vs MT5
    if "Deal" in text[:500] or "Direction" in text[:500]:
        trades_data = parse_mt5_csv(text, account_id)
        format_used = "MT5"
    else:
        trades_data = parse_mt4_csv(text, account_id)
        format_used = "MT4"
    
    if not trades_data:
        raise HTTPException(status_code=400, detail="No valid trades found in file")
    
    imported = 0
    for trade_data in trades_data:
        try:
            trade = Trade(**{k: v for k, v in trade_data.items() if v is not None})
            db.add(trade)
            db.commit()
            imported += 1
        except Exception as e:
            db.rollback()
            continue
    
    return {
        "success": True,
        "format": format_used,
        "imported": imported,
        "total": len(trades_data),
        "message": f"{imported} trades importés depuis {format_used}"
    }

@router.post("/csv")
async def import_csv(
    file: UploadFile = File(...),
    account_id: int = 1,
    db: Session = Depends(get_db)
):
    """Import trades from generic CSV"""
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    
    # Try MT5 first, then MT4
    trades_data = parse_mt5_csv(text, account_id)
    if not trades_data:
        trades_data = parse_mt4_csv(text, account_id)
    
    if not trades_data:
        raise HTTPException(status_code=400, detail="Format non reconnu")
    
    imported = 0
    for trade_data in trades_data:
        try:
            trade = Trade(**{k: v for k, v in trade_data.items() if v is not None})
            db.add(trade)
            db.commit()
            imported += 1
        except:
            db.rollback()
            continue
    
    return {"success": True, "imported": imported, "total": len(trades_data)}
