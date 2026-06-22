"""
Statistics calculator service
Handles all trading performance calculations
"""
from typing import List
from models import Trade


class StatsCalculator:
    """
    Calculator for trading statistics and metrics
    """
    
    def calculate_win_rate(self, trades: List[Trade]) -> float:
        """
        Calculate win rate percentage
        """
        if not trades:
            return 0.0
        
        winning_trades = [t for t in trades if t.result == "WIN"]
        return (len(winning_trades) / len(trades)) * 100
    
    def calculate_profit_factor(self, trades: List[Trade]) -> float:
        """
        Calculate profit factor (gross profit / gross loss)
        """
        if not trades:
            return 0.0
        
        gross_profit = sum(t.profit_loss for t in trades if t.profit_loss > 0)
        gross_loss = abs(sum(t.profit_loss for t in trades if t.profit_loss < 0))
        
        if gross_loss == 0:
            return gross_profit if gross_profit > 0 else 0.0
        
        return gross_profit / gross_loss
    
    def calculate_average_rr(self, trades: List[Trade]) -> float:
        """
        Calculate average risk:reward ratio
        """
        if not trades:
            return 0.0
        
        trades_with_rr = [t for t in trades if t.rr_obtained is not None]
        
        if not trades_with_rr:
            return 0.0
        
        total_rr = sum(t.rr_obtained for t in trades_with_rr)
        return total_rr / len(trades_with_rr)
    
    def calculate_expectancy(self, trades: List[Trade]) -> float:
        """
        Calculate expectancy (average profit/loss per trade)
        """
        if not trades:
            return 0.0
        
        total_profit_loss = sum(t.profit_loss for t in trades)
        return total_profit_loss / len(trades)
    
    def calculate_max_drawdown(self, trades: List[Trade]) -> float:
        """
        Calculate maximum drawdown percentage
        """
        if not trades:
            return 0.0
        
        # Sort trades by date
        sorted_trades = sorted(trades, key=lambda t: t.trade_date)
        
        peak = 0.0
        running_balance = 0.0
        max_drawdown = 0.0
        
        for trade in sorted_trades:
            running_balance += trade.profit_loss
            
            if running_balance > peak:
                peak = running_balance
            
            drawdown = ((peak - running_balance) / peak) * 100 if peak > 0 else 0.0
            
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        return max_drawdown
    
    def calculate_current_drawdown(self, trades: List[Trade]) -> float:
        """
        Calculate current drawdown percentage from peak
        """
        if not trades:
            return 0.0
        
        # Sort trades by date
        sorted_trades = sorted(trades, key=lambda t: t.trade_date)
        
        peak = 0.0
        running_balance = 0.0
        
        for trade in sorted_trades:
            running_balance += trade.profit_loss
            
            if running_balance > peak:
                peak = running_balance
        
        if peak == 0:
            return 0.0
        
        return ((peak - running_balance) / peak) * 100
    
    def calculate_trading_score(self, trade) -> int:
        """
        Calculate trading score (0-100) based on:
        - plan_respected (30 pts)
        - confidence_level (20 pts)
        - discipline_felt (20 pts)
        - rr_obtained vs rr_planned (30 pts)
        """
        score = 0
        
        # Plan respected (30 pts)
        if trade.plan_respected:
            score += 30
        
        # Confidence level (20 pts) - scale 1-10 to 0-20
        if trade.confidence_level:
            score += (trade.confidence_level / 10) * 20
        
        # Discipline felt (20 pts) - convert to numeric
        if trade.discipline_felt:
            discipline_scores = {
                "excellent": 20,
                "good": 15,
                "average": 10,
                "poor": 5,
                "terrible": 0
            }
            score += discipline_scores.get(trade.discipline_felt.lower(), 10)
        
        # RR obtained vs planned (30 pts)
        if trade.rr_planned and trade.rr_obtained:
            rr_ratio = trade.rr_obtained / trade.rr_planned if trade.rr_planned > 0 else 0
            if rr_ratio >= 1.0:
                score += 30
            elif rr_ratio >= 0.8:
                score += 25
            elif rr_ratio >= 0.5:
                score += 15
            elif rr_ratio >= 0.3:
                score += 5
        elif trade.rr_obtained and trade.rr_obtained > 0:
            score += 15  # Partial credit for positive RR
        
        return min(int(score), 100)
    
    def calculate_all_stats(self, trades: List[Trade]) -> dict:
        """
        Calculate all statistics and return as dictionary
        """
        if not trades:
            return {
                "total_trades": 0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "average_rr": 0.0,
                "expectancy": 0.0,
                "max_drawdown": 0.0,
                "current_drawdown": 0.0,
                "total_profit": 0.0,
                "total_loss": 0.0,
                "net_profit": 0.0,
                "average_trading_score": 0.0,
                "plan_respect_rate": 0.0
            }
        
        total_profit = sum(t.profit_loss for t in trades if t.profit_loss > 0)
        total_loss = abs(sum(t.profit_loss for t in trades if t.profit_loss < 0))
        net_profit = sum(t.profit_loss for t in trades)
        
        plan_respected_trades = [t for t in trades if t.plan_respected]
        plan_respect_rate = (len(plan_respected_trades) / len(trades)) * 100 if trades else 0.0
        
        avg_score = sum(t.trading_score for t in trades) / len(trades) if trades else 0.0
        
        return {
            "total_trades": len(trades),
            "win_rate": self.calculate_win_rate(trades),
            "profit_factor": self.calculate_profit_factor(trades),
            "average_rr": self.calculate_average_rr(trades),
            "expectancy": self.calculate_expectancy(trades),
            "max_drawdown": self.calculate_max_drawdown(trades),
            "current_drawdown": self.calculate_current_drawdown(trades),
            "total_profit": total_profit,
            "total_loss": total_loss,
            "net_profit": net_profit,
            "average_trading_score": avg_score,
            "plan_respect_rate": plan_respect_rate
        }
