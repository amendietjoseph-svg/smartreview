"""
AI Service for SmartReview
Handles AI-powered trading analysis using Claude API
"""
import httpx
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from models import Trade, Account
import os
from dotenv import load_dotenv

load_dotenv()


class AIService:
    """
    Service for AI-powered trading analysis and recommendations
    Uses Claude API via httpx
    """
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-haiku-4-5"
        self.system_prompt = """Tu es SmartReview AI Coach, un expert en analyse de trading quantitatif.
Tu analyses les données de trading d'un trader pour identifier ses forces,
faiblesses, patterns et edge statistique.
Réponds toujours en français, de manière structurée avec des sections claires.
Sois précis, data-driven, et bienveillant mais direct."""
    
    async def analyze_performance(self, trades: List[Trade], account: Account, period: str = "30d") -> str:
        """
        Analyze trading performance using Claude API
        Returns comprehensive analysis as markdown string
        """
        if not trades:
            return "# Aucune donnée disponible\n\nCommencez à enregistrer vos trades pour obtenir une analyse personnalisée."
        
        # Filter trades by period
        filtered_trades = self._filter_trades_by_period(trades, period)
        
        if not filtered_trades:
            return "# Aucune donnée pour cette période\n\nAucun trade trouvé sur la période sélectionnée."
        
        # Calculate statistics
        stats = self._calculate_comprehensive_stats(filtered_trades)
        
        # Build user prompt
        user_prompt = self._build_analysis_prompt(stats, filtered_trades, period)
        
        # Call Claude API
        try:
            return await self._call_claude_api_streaming(user_prompt)
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            # Fallback to rule-based analysis
            return self._generate_rule_based_analysis(stats, filtered_trades)
    
    def _filter_trades_by_period(self, trades: List[Trade], period: str) -> List[Trade]:
        """Filter trades by time period"""
        if period == "all":
            return trades
        
        now = datetime.now()
        period_map = {
            "7d": timedelta(days=7),
            "30d": timedelta(days=30),
            "90d": timedelta(days=90),
            "1y": timedelta(days=365)
        }
        
        delta = period_map.get(period, timedelta(days=30))
        cutoff = now - delta
        
        return [t for t in trades if t.trade_date and datetime.fromisoformat(t.trade_date.replace('Z', '+00:00')) >= cutoff]
    
    def _calculate_comprehensive_stats(self, trades: List[Trade]) -> Dict:
        """Calculate comprehensive trading statistics"""
        if not trades:
            return {}
        
        wins = [t for t in trades if t.result == "WIN"]
        losses = [t for t in trades if t.result == "LOSS"]
        breakevens = [t for t in trades if t.result == "BREAKEVEN"]
        
        total_trades = len(trades)
        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0
        
        # P&L stats
        total_pnl = sum(t.profit_loss for t in trades)
        avg_pnl = total_pnl / total_trades if total_trades > 0 else 0
        
        # RR stats
        trades_with_rr = [t for t in trades if t.rr_obtained is not None]
        avg_rr = sum(t.rr_obtained for t in trades_with_rr) / len(trades_with_rr) if trades_with_rr else 0
        
        # Profit factor
        total_wins_pnl = sum(t.profit_loss for t in wins)
        total_losses_pnl = abs(sum(t.profit_loss for t in losses))
        profit_factor = total_wins_pnl / total_losses_pnl if total_losses_pnl > 0 else 0
        
        # Expectancy
        expectancy = total_pnl / total_trades if total_trades > 0 else 0
        
        # Drawdown
        cumulative = []
        running_pnl = 0
        for t in sorted(trades, key=lambda x: x.trade_date or ""):
            running_pnl += t.profit_loss
            cumulative.append(running_pnl)
        
        max_drawdown = 0
        peak = 0
        for val in cumulative:
            if val > peak:
                peak = val
            dd = (peak - val) / peak if peak > 0 else 0
            max_drawdown = max(max_drawdown, dd)
        
        # Trading score
        avg_score = sum(t.trading_score for t in trades if t.trading_score) / len([t for t in trades if t.trading_score]) if any(t.trading_score for t in trades) else 0
        
        # Setup distribution
        setup_dist = defaultdict(lambda: {"wins": 0, "total": 0, "pnl": 0})
        for t in trades:
            if t.setup:
                setup_dist[t.setup]["total"] += 1
                setup_dist[t.setup]["pnl"] += t.profit_loss
                if t.result == "WIN":
                    setup_dist[t.setup]["wins"] += 1
        
        # Session distribution
        session_dist = defaultdict(lambda: {"wins": 0, "total": 0, "pnl": 0})
        for t in trades:
            if t.session:
                session_dist[t.session]["total"] += 1
                session_dist[t.session]["pnl"] += t.profit_loss
                if t.result == "WIN":
                    session_dist[t.session]["wins"] += 1
        
        # Asset distribution
        asset_dist = defaultdict(lambda: {"wins": 0, "total": 0, "pnl": 0})
        for t in trades:
            asset_dist[t.asset]["total"] += 1
            asset_dist[t.asset]["pnl"] += t.profit_loss
            if t.result == "WIN":
                asset_dist[t.asset]["wins"] += 1
        
        # Psychological stats
        emotions = defaultdict(int)
        for t in trades:
            if t.emotional_state:
                emotions[t.emotional_state] += 1
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else "N/A"
        
        plan_respected = [t for t in trades if t.plan_respected]
        plan_rate = (len(plan_respected) / total_trades * 100) if total_trades > 0 else 0
        
        confidence_avg = sum(t.confidence_level for t in trades if t.confidence_level) / len([t for t in trades if t.confidence_level]) if any(t.confidence_level for t in trades) else 0
        
        # Trades outside strategy
        outside_strategy = [t for t in trades if not t.plan_respected]
        outside_pnl = sum(t.profit_loss for t in outside_strategy)
        
        return {
            "total_trades": total_trades,
            "win_rate": win_rate,
            "profit_factor": profit_factor,
            "avg_rr": avg_rr,
            "expectancy": expectancy,
            "max_drawdown": max_drawdown * 100,
            "avg_score": avg_score,
            "setup_dist": dict(setup_dist),
            "session_dist": dict(session_dist),
            "asset_dist": dict(asset_dist),
            "dominant_emotion": dominant_emotion,
            "plan_rate": plan_rate,
            "confidence_avg": confidence_avg,
            "outside_strategy_count": len(outside_strategy),
            "outside_strategy_pnl": outside_pnl
        }
    
    def _build_analysis_prompt(self, stats: Dict, trades: List[Trade], period: str) -> str:
        """Build the analysis prompt for Claude"""
        prompt = f"""Voici les données de trading du trader sur les {period} derniers trades :

STATISTIQUES GLOBALES :
- Win Rate : {stats['win_rate']:.1f}%
- Profit Factor : {stats['profit_factor']:.2f}
- RR Moyen : {stats['avg_rr']:.2f}
- Espérance : ${stats['expectancy']:.2f}
- Drawdown Max : {stats['max_drawdown']:.1f}%
- Trading Score moyen : {stats['avg_score']:.1f}/100

RÉPARTITION PAR SETUP :
"""
        for setup, data in stats['setup_dist'].items():
            wr = (data['wins'] / data['total'] * 100) if data['total'] > 0 else 0
            prompt += f"- {setup}: {data['total']} trades, WR: {wr:.1f}%, P&L: ${data['pnl']:.2f}\n"
        
        prompt += "\nRÉPARTITION PAR SESSION :\n"
        for session, data in stats['session_dist'].items():
            wr = (data['wins'] / data['total'] * 100) if data['total'] > 0 else 0
            prompt += f"- {session}: {data['total']} trades, WR: {wr:.1f}%, P&L: ${data['pnl']:.2f}\n"
        
        prompt += "\nRÉPARTITION PAR ACTIF :\n"
        for asset, data in stats['asset_dist'].items():
            wr = (data['wins'] / data['total'] * 100) if data['total'] > 0 else 0
            prompt += f"- {asset}: {data['total']} trades, WR: {wr:.1f}%, P&L: ${data['pnl']:.2f}\n"
        
        prompt += f"""
DONNÉES PSYCHOLOGIQUES :
- État émotionnel dominant : {stats['dominant_emotion']}
- Respect du plan : {stats['plan_rate']:.1f}%
- Confiance moyenne : {stats['confidence_avg']:.1f}/10

TRADES HORS STRATÉGIE :
- Nombre : {stats['outside_strategy_count']}
- Impact financier : ${stats['outside_strategy_pnl']:.2f}

Produis une analyse complète avec :
1. Résumé des performances (3-4 phrases)
2. Forces identifiées (liste avec données)
3. Faiblesses et comportements limitants (liste avec données)
4. Patterns détectés (corrélations intéressantes)
5. Recommandations concrètes (5 actions prioritaires)
6. Score de progression (X/100 avec explication)"""
        
        return prompt
    
    def _generate_rule_based_analysis(self, stats: Dict, trades: List[Trade]) -> str:
        """Generate rule-based analysis as fallback"""
        analysis = "# Analyse de Performance\n\n"
        
        # Summary
        analysis += "## Résumé des Performances\n\n"
        analysis += f"Sur {stats['total_trades']} trades, vous affichez un Win Rate de {stats['win_rate']:.1f}% "
        analysis += f"avec une espérance de ${stats['expectancy']:.2f} par trade. "
        
        if stats['win_rate'] >= 50:
            analysis += "Votre performance globale est positive. "
        else:
            analysis += "Votre performance nécessite des ajustements. "
        
        analysis += f"Le drawdown maximum est de {stats['max_drawdown']:.1f}%.\n\n"
        
        # Strengths
        analysis += "## Forces Identifiées\n\n"
        if stats['win_rate'] >= 50:
            analysis += f"- **Win Rate solide**: {stats['win_rate']:.1f}% de trades gagnants\n"
        if stats['avg_rr'] >= 1.5:
            analysis += f"- **Gestion du risque**: RR moyen de {stats['avg_rr']:.2f}\n"
        if stats['plan_rate'] >= 70:
            analysis += f"- **Discipline**: Plan respecté dans {stats['plan_rate']:.1f}% des cas\n"
        if stats['avg_score'] >= 60:
            analysis += f"- **Processus**: Score de trading moyen de {stats['avg_score']:.1f}/100\n"
        
        if analysis.endswith("## Forces Identifiées\n\n"):
            analysis += "Pas assez de données pour identifier des forces claires.\n"
        
        analysis += "\n"
        
        # Weaknesses
        analysis += "## Faiblesses et Comportements Limitants\n\n"
        if stats['win_rate'] < 50:
            analysis += f"- **Win Rate insuffisant**: {stats['win_rate']:.1f}% est en dessous du seuil de rentabilité\n"
        if stats['avg_rr'] < 1:
            analysis += f"- **RR trop faible**: Moyenne de {stats['avg_rr']:.2f}, visez 2:1 minimum\n"
        if stats['plan_rate'] < 70:
            analysis += f"- **Discipline variable**: Plan respecté seulement {stats['plan_rate']:.1f}% du temps\n"
        if stats['outside_strategy_count'] > 0:
            analysis += f"- **Trades hors stratégie**: {stats['outside_strategy_count']} trades impactant ${stats['outside_strategy_pnl']:.2f}\n"
        if stats['max_drawdown'] > 20:
            analysis += f"- **Gestion du drawdown**: Maximum de {stats['max_drawdown']:.1f}% est élevé\n"
        
        if analysis.endswith("## Faiblesses et Comportements Limitants\n\n"):
            analysis += "Pas de faiblesses majeures détectées.\n"
        
        analysis += "\n"
        
        # Patterns
        analysis += "## Patterns Détectés\n\n"
        
        # Best setup
        if stats['setup_dist']:
            best_setup = max(stats['setup_dist'].items(), key=lambda x: x[1]['pnl'])
            analysis += f"- **Setup le plus rentable**: {best_setup[0]} avec ${best_setup[1]['pnl']:.2f}\n"
        
        # Best session
        if stats['session_dist']:
            best_session = max(stats['session_dist'].items(), key=lambda x: x[1]['pnl'])
            analysis += f"- **Session la plus rentable**: {best_session[0]} avec ${best_session[1]['pnl']:.2f}\n"
        
        # Best asset
        if stats['asset_dist']:
            best_asset = max(stats['asset_dist'].items(), key=lambda x: x[1]['pnl'])
            analysis += f"- **Actif le plus rentable**: {best_asset[0]} avec ${best_asset[1]['pnl']:.2f}\n"
        
        analysis += "\n"
        
        # Recommendations
        analysis += "## Recommandations Concrètes\n\n"
        analysis += "1. **Focus sur vos meilleurs setups**: Augmentez la taille de position sur vos setups les plus rentables\n"
        analysis += "2. **Améliorer la discipline**: Respectez strictement votre plan de trading\n"
        if stats['avg_rr'] < 1.5:
            analysis += "3. **Viser un RR plus élevé**: Cherchez des setups avec potentiel 2:1 ou mieux\n"
        if stats['plan_rate'] < 70:
            analysis += "4. **Journal de trading**: Notez pourquoi vous sortez de votre plan\n"
        analysis += "5. **Gestion des émotions**: Travaillez sur votre état psychologique avant de trader\n"
        
        # Progression score
        progression_score = int(
            (stats['win_rate'] / 100 * 30) +
            (min(stats['avg_rr'] / 2, 1) * 30) +
            (stats['plan_rate'] / 100 * 20) +
            (stats['avg_score'] / 100 * 20)
        )
        
        analysis += f"\n## Score de Progression\n\n**{progression_score}/100**\n\n"
        analysis += f"Ce score reflète votre progression globale basée sur votre Win Rate ({stats['win_rate']:.1f}%), "
        analysis += f"votre gestion du risque (RR: {stats['avg_rr']:.2f}), votre discipline ({stats['plan_rate']:.1f}%) "
        analysis += f"et la qualité de votre processus (Score: {stats['avg_score']:.1f})."
        
        return analysis
    
    def detect_edge(self, trades: List[Trade]) -> List[Dict]:
        """
        Detect statistical edges by crossing all variables
        Returns top 5 edges with composite scores
        """
        if not trades:
            return []
        
        edges = []
        
        # Get unique values for each dimension
        assets = list(set(t.asset for t in trades))
        setups = list(set(t.setup for t in trades if t.setup))
        sessions = list(set(t.session for t in trades if t.session))
        
        # Get hours from entry times
        hours = list(set(
            datetime.fromisoformat(t.entry_time.replace('Z', '+00:00')).hour 
            for t in trades if t.entry_time
        ))
        
        # Generate combinations (limit to avoid explosion)
        # Focus on asset × setup × session combinations
        for asset in assets:
            for setup in setups:
                for session in sessions:
                    combo_trades = [
                        t for t in trades 
                        if t.asset == asset and t.setup == setup and t.session == session
                    ]
                    
                    if len(combo_trades) >= 5:  # Minimum 5 trades
                        edge = self._calculate_edge_score(combo_trades, {
                            "asset": asset,
                            "setup": setup,
                            "session": session
                        })
                        edges.append(edge)
        
        # Sort by composite score
        edges.sort(key=lambda x: x["composite_score"], reverse=True)
        
        return edges[:5]
    
    def _calculate_edge_score(self, trades: List[Trade], dimensions: Dict) -> Dict:
        """Calculate edge score for a combination"""
        wins = [t for t in trades if t.result == "WIN"]
        total = len(trades)
        
        win_rate = (len(wins) / total * 100) if total > 0 else 0
        avg_rr = sum(t.rr_obtained for t in trades if t.rr_obtained) / len([t for t in trades if t.rr_obtained]) if any(t.rr_obtained for t in trades) else 0
        total_pnl = sum(t.profit_loss for t in trades)
        
        # Profit factor
        total_wins_pnl = sum(t.profit_loss for t in wins)
        total_losses_pnl = abs(sum(t.profit_loss for t in trades if t.result == "LOSS"))
        profit_factor = total_wins_pnl / total_losses_pnl if total_losses_pnl > 0 else 0
        
        # Composite score: win_rate (40%) + rr (30%) + profit_factor (30%)
        composite_score = (win_rate / 100 * 40) + (min(avg_rr / 2, 1) * 30) + (min(profit_factor / 2, 1) * 30)
        
        return {
            "dimensions": dimensions,
            "win_rate": win_rate,
            "avg_rr": avg_rr,
            "total_pnl": total_pnl,
            "total_trades": total,
            "profit_factor": profit_factor,
            "composite_score": composite_score
        }
    
    async def generate_daily_report(self, trades_today: List[Trade], historical_trades: List[Trade]) -> str:
        """Generate daily report comparing today's performance to historical average"""
        if not trades_today:
            return "# Rapport du Jour\n\nAucun trade effectué aujourd'hui."
        
        # Calculate today's stats
        today_stats = self._calculate_comprehensive_stats(trades_today)
        
        # Calculate historical stats
        hist_stats = self._calculate_comprehensive_stats(historical_trades) if historical_trades else {}
        
        report = "# Rapport du Jour\n\n"
        report += f"**Date**: {datetime.now().strftime('%d/%m/%Y')}\n"
        report += f"**Trades aujourd'hui**: {len(trades_today)}\n\n"
        
        # Performance comparison
        report += "## Performance vs Moyenne Historique\n\n"
        if hist_stats:
            report += f"- **Win Rate aujourd'hui**: {today_stats['win_rate']:.1f}% (moyenne: {hist_stats['win_rate']:.1f}%)\n"
            report += f"- **RR moyen aujourd'hui**: {today_stats['avg_rr']:.2f} (moyenne: {hist_stats['avg_rr']:.2f})\n"
            report += f"- **P&L aujourd'hui**: ${today_stats['expectancy'] * len(trades_today):.2f}\n"
        else:
            report += f"- **Win Rate aujourd'hui**: {today_stats['win_rate']:.1f}%\n"
            report += f"- **RR moyen aujourd'hui**: {today_stats['avg_rr']:.2f}\n"
            report += f"- **P&L aujourd'hui**: ${today_stats['expectancy'] * len(trades_today):.2f}\n"
        
        # Strategy respect
        report += "\n## Respect de la Stratégie\n\n"
        plan_respected_today = len([t for t in trades_today if t.plan_respected])
        plan_rate_today = (plan_respected_today / len(trades_today) * 100) if trades_today else 0
        report += f"Plan respecté: {plan_rate_today:.1f}% des trades aujourd'hui\n"
        
        # Psychological state
        report += "\n## État Psychologique\n\n"
        emotions_today = defaultdict(int)
        for t in trades_today:
            if t.emotional_state:
                emotions_today[t.emotional_state] += 1
        
        if emotions_today:
            dominant_emotion = max(emotions_today.items(), key=lambda x: x[1])[0]
            report += f"État émotionnel dominant: {dominant_emotion}\n"
            
            # Impact on performance
            emotion_trades = [t for t in trades_today if t.emotional_state == dominant_emotion]
            emotion_wr = (len([t for t in emotion_trades if t.result == "WIN"]) / len(emotion_trades) * 100) if emotion_trades else 0
            report += f"Win Rate dans cet état: {emotion_wr:.1f}%\n"
        
        # Key takeaways
        report += "\n## Points à Retenir pour Demain\n\n"
        if today_stats['win_rate'] >= 50:
            report += "1. Continuez avec votre approche actuelle, elle fonctionne bien.\n"
        else:
            report += "1. Revoyez vos critères d'entrée avant de trader demain.\n"
        
        if plan_rate_today < 80:
            report += "2. Renforcez votre discipline en respectant strictement votre plan.\n"
        
        if today_stats['avg_rr'] < 1.5:
            report += "3. Cherchez des setups avec un meilleur ratio risque/récompense.\n"
        
        report += "4. Notez vos émotions et leur impact sur vos décisions.\n"
        report += "5. Préparez votre séance à l'avance pour éviter les trades impulsifs.\n"
        
        return report
    
    async def generate_weekly_summary(self, trades_week: List[Trade]) -> str:
        """Generate weekly summary with trends and advice"""
        if not trades_week:
            return "# Résumé Hebdomadaire\n\nAucun trade cette semaine."
        
        stats = self._calculate_comprehensive_stats(trades_week)
        
        summary = "# Résumé Hebdomadaire\n\n"
        summary += f"**Période**: {datetime.now().strftime('%d/%m/%Y')}\n"
        summary += f"**Trades cette semaine**: {len(trades_week)}\n\n"
        
        # Performance overview
        summary += "## Performance Globale\n\n"
        summary += f"- **Win Rate**: {stats['win_rate']:.1f}%\n"
        summary += f"- **P&L total**: ${sum(t.profit_loss for t in trades_week):.2f}\n"
        summary += f"- **RR moyen**: {stats['avg_rr']:.2f}\n"
        summary += f"- **Trading Score moyen**: {stats['avg_score']:.1f}/100\n\n"
        
        # Best performers
        summary += "## Meilleurs Performeurs\n\n"
        if stats['setup_dist']:
            best_setup = max(stats['setup_dist'].items(), key=lambda x: x[1]['pnl'])
            summary += f"- **Setup**: {best_setup[0]} (${best_setup[1]['pnl']:.2f})\n"
        
        if stats['session_dist']:
            best_session = max(stats['session_dist'].items(), key=lambda x: x[1]['pnl'])
            summary += f"- **Session**: {best_session[0]} (${best_session[1]['pnl']:.2f})\n"
        
        if stats['asset_dist']:
            best_asset = max(stats['asset_dist'].items(), key=lambda x: x[1]['pnl'])
            summary += f"- **Actif**: {best_asset[0]} (${best_asset[1]['pnl']:.2f})\n"
        
        # Trends
        summary += "\n## Tendances et Conseils\n\n"
        
        if stats['win_rate'] >= 60:
            summary += "✅ Excellente semaine! Votre stratégie fonctionne bien.\n"
            summary += "Continuez à vous concentrer sur vos setups les plus rentables.\n"
        elif stats['win_rate'] >= 40:
            summary += "⚠️ Semaine mitigée. Identifiez ce qui a fonctionné et ce qui n'a pas.\n"
            summary += "Revoyez vos trades perdants pour trouver des patterns.\n"
        else:
            summary += "❌ Semaine difficile. Il est temps de revoir votre approche.\n"
            summary += "Réduisez votre taille de position et concentrez-vous sur la qualité.\n"
        
        if stats['plan_rate'] < 70:
            summary += "\n⚠️ Discipline en baisse. Revenez aux bases de votre plan.\n"
        
        summary += "\n## Objectifs pour la Semaine Prochaine\n\n"
        summary += "1. Maintenir ou améliorer le Win Rate actuel\n"
        summary += "2. Augmenter le RR moyen en visant des setups de meilleure qualité\n"
        summary += "3. Respecter le plan de trading à 100%\n"
        summary += "4. Noter systématiquement l'état émotionnel avant chaque trade\n"
        
        return summary
    
    async def _call_claude_api_streaming(self, prompt: str) -> str:
        """Call Claude API with streaming support"""
        if not self.api_key:
            raise ValueError("Claude API key not configured. Set ANTHROPIC_API_KEY in .env file")
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": self.model,
            "max_tokens": 4096,
            "system": self.system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.api_url,
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
