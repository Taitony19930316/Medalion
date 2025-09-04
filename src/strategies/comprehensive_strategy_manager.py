"""
综合策略管理器 - 整合缠论策略、AI功能和策略跟踪
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from .changlun_strategy import ChangLunStrategy, TrendDirection, RelativePosition
from .strategy_tracker import StrategyTracker, TrackedTrader, TrackingMode
from .strategy_tree import StrategyTree
from ..ai.ai_manager import AIManager

@dataclass
class StrategyPerformance:
    """策略表现数据"""
    strategy_name: str
    total_trades: int
    win_rate: float
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    last_update: datetime

class ComprehensiveStrategyManager:
    """综合策略管理器"""
    
    def __init__(self, ai_config: Dict[str, Any] = None):
        # 核心组件
        self.changlun_strategy = ChangLunStrategy()
        self.strategy_tracker = StrategyTracker()
        self.strategy_tree = StrategyTree()
        self.ai_manager = AIManager(ai_config) if ai_config else None
        
        # 策略表现跟踪
        self.strategy_performances: Dict[str, StrategyPerformance] = {}
        
        # 当前持仓和信号
        self.current_positions: Dict[str, Dict] = {}
        self.recent_signals: List[Dict] = []
        
        # 配置参数
        self.max_positions = 10
        self.total_capital = 1000000  # 100万初始资金
        
    def analyze_market_with_changlun(self, symbol: str, data: pd.DataFrame) -> Dict[str, Any]:
        """使用缠论分析市场"""
        
        # 获取缠论策略状态
        strategy_status = self.changlun_strategy.get_strategy_status(data)
        
        # 计算交易信号
        signal = self.changlun_strategy.calculate_signal(data)
        
        # 如果有信号，计算建议仓位
        suggested_position = 0
        if signal:
            suggested_position = self.changlun_strategy.calculate_position_size(signal, data)
        
        analysis_result = {
            'symbol': symbol,
            'timestamp': datetime.now(),
            'strategy_status': strategy_status,
            'signal': {
                'type': signal.signal_type.name if signal else 'HOLD',
                'strength': signal.strength.name if signal else 'NONE',
                'confidence': signal.confidence if signal else 0,
                'reason': signal.reason if signal else '无信号',
                'suggested_position': suggested_position
            },
            'market_analysis': {
                'trend_direction': strategy_status.get('trend_direction', 'UNKNOWN'),
                'relative_position': strategy_status.get('relative_position', 'UNKNOWN'),
                'divergence_signal': strategy_status.get('divergence_signal'),
                'rsi_value': strategy_status.get('rsi_value', 50),
                'emotion_extreme': strategy_status.get('emotion_extreme', False)
            }
        }
        
        return analysis_result
    
    def get_ai_enhanced_analysis(self, symbol: str, data: pd.DataFrame, 
                               recent_trades: pd.DataFrame = None) -> Dict[str, Any]:
        """获取AI增强分析"""
        if not self.ai_manager:
            return {'error': 'AI功能未启用'}
        
        try:
            # 1. 基础缠论分析
            changlun_analysis = self.analyze_market_with_changlun(symbol, data)
            
            # 2. AI置信度评估
            market_indicators = {
                'volatility': data['close'].pct_change().std(),
                'trend_strength': 0.7,  # 可以根据实际情况计算
                'sentiment': 0.6
            }
            
            confidence_eval = self.ai_manager.evaluate_strategy_confidence(
                strategy_name="缠论策略",
                market_data={symbol: data},
                recent_signals=recent_trades if recent_trades is not None else pd.DataFrame(),
                market_indicators=market_indicators
            )
            
            # 3. AI股票筛选评分
            stock_screening = self.ai_manager.screen_stocks_intelligently(
                stock_pool=[symbol],
                strategy_requirements={
                    'strategy_type': '缠论MACD策略',
                    'timeframe': '日线',
                    'risk_tolerance': '中等'
                },
                market_data={symbol: data}
            )
            
            # 4. 综合AI洞察
            ai_insights = self.ai_manager.get_ai_insights(
                trades_df=recent_trades,
                market_data={symbol: data},
                strategy_name="缠论策略"
            )
            
            return {
                'changlun_analysis': changlun_analysis,
                'ai_confidence': confidence_eval,
                'ai_screening': stock_screening,
                'ai_insights': ai_insights,
                'enhanced_recommendation': self._generate_enhanced_recommendation(
                    changlun_analysis, confidence_eval, stock_screening
                )
            }
            
        except Exception as e:
            return {'error': f'AI分析失败: {str(e)}'}
    
    def _generate_enhanced_recommendation(self, changlun_analysis: Dict, 
                                        confidence_eval: Dict, 
                                        screening_result: Dict) -> Dict[str, Any]:
        """生成增强推荐"""
        
        # 缠论信号
        changlun_signal = changlun_analysis['signal']
        changlun_confidence = changlun_signal['confidence']
        
        # AI置信度
        ai_confidence = confidence_eval.get('overall_confidence', 0.5)
        
        # 筛选评分
        screening_confidence = 0.5
        if 'confidence_scores' in screening_result:
            symbol = changlun_analysis['symbol']
            screening_confidence = screening_result['confidence_scores'].get(symbol, 0.5)
        
        # 综合评分
        combined_confidence = (changlun_confidence * 0.4 + 
                             ai_confidence * 0.4 + 
                             screening_confidence * 0.2)
        
        # 生成最终建议
        if combined_confidence >= 0.75:
            recommendation = "强烈推荐"
            action = changlun_signal['type']
            position_size = changlun_signal['suggested_position'] * 1.2  # 增加仓位
        elif combined_confidence >= 0.6:
            recommendation = "推荐"
            action = changlun_signal['type']
            position_size = changlun_signal['suggested_position']
        elif combined_confidence >= 0.4:
            recommendation = "谨慎观望"
            action = "HOLD"
            position_size = changlun_signal['suggested_position'] * 0.5  # 减少仓位
        else:
            recommendation = "不推荐"
            action = "HOLD"
            position_size = 0
        
        return {
            'recommendation': recommendation,
            'action': action,
            'combined_confidence': combined_confidence,
            'suggested_position_size': min(position_size, 0.3),  # 最大30%仓位
            'reasoning': [
                f"缠论信号: {changlun_signal['type']} (置信度: {changlun_confidence:.2f})",
                f"AI评估: {confidence_eval.get('recommendation', 'N/A')} (置信度: {ai_confidence:.2f})",
                f"筛选评分: {screening_confidence:.2f}",
                f"综合评分: {combined_confidence:.2f}"
            ]
        }
    
    def track_external_strategy(self, trader_info: Dict[str, Any]) -> str:
        """开始跟踪外部策略"""
        
        trader = TrackedTrader(
            trader_id=trader_info['trader_id'],
            name=trader_info['name'],
            platform=trader_info.get('platform', 'unknown'),
            win_rate=trader_info.get('win_rate', 0.5),
            total_return=trader_info.get('total_return', 0.0),
            max_drawdown=trader_info.get('max_drawdown', 0.0),
            tracking_start_date=datetime.now()
        )
        
        self.strategy_tracker.add_trader_to_track(trader)
        
        return f"开始跟踪策略: {trader.name}"
    
    def update_tracked_strategy_trades(self, trader_id: str, trades: List[Dict]):
        """更新被跟踪策略的交易记录"""
        self.strategy_tracker.update_trader_trades(trader_id, trades)
        
        # 生成跟单信号
        signals = self.strategy_tracker.get_real_time_signals(
            trader_id, TrackingMode.DELAYED
        )
        
        # 将信号添加到策略树
        for signal in signals:
            self._process_tracking_signal(signal)
    
    def _process_tracking_signal(self, signal: Dict):
        """处理跟踪信号"""
        
        # 验证信号有效性
        if signal['confidence'] < 0.3:
            return  # 置信度太低，忽略
        
        # 检查是否与现有策略冲突
        conflict_check = self._check_signal_conflicts(signal)
        
        if not conflict_check['has_conflict']:
            # 添加到待执行信号列表
            enhanced_signal = {
                **signal,
                'source': 'tracking',
                'processed_time': datetime.now(),
                'validation_passed': True
            }
            
            self.recent_signals.append(enhanced_signal)
    
    def _check_signal_conflicts(self, new_signal: Dict) -> Dict[str, Any]:
        """检查信号冲突"""
        
        symbol = new_signal['symbol']
        action = new_signal['action']
        
        # 检查是否已有该股票的持仓
        current_position = self.current_positions.get(symbol)
        
        conflicts = []
        
        if current_position:
            if action == 'BUY' and current_position['quantity'] > 0:
                conflicts.append("已有多头持仓，重复买入信号")
            elif action == 'SELL' and current_position['quantity'] < 0:
                conflicts.append("已有空头持仓，重复卖出信号")
        
        # 检查与最近信号的冲突
        recent_same_symbol_signals = [
            s for s in self.recent_signals[-10:] 
            if s.get('symbol') == symbol and 
            (datetime.now() - s.get('processed_time', datetime.now())).seconds < 3600
        ]
        
        if recent_same_symbol_signals:
            last_signal = recent_same_symbol_signals[-1]
            if last_signal.get('action') == action:
                conflicts.append("1小时内有相同方向信号")
        
        return {
            'has_conflict': len(conflicts) > 0,
            'conflicts': conflicts,
            'can_execute': len(conflicts) == 0
        }
    
    def generate_daily_strategy_report(self, date: datetime = None) -> Dict[str, Any]:
        """生成每日策略报告"""
        
        if date is None:
            date = datetime.now()
        
        report = {
            'date': date.strftime('%Y-%m-%d'),
            'summary': {
                'total_strategies': len(self.strategy_performances),
                'active_positions': len(self.current_positions),
                'signals_generated': len([s for s in self.recent_signals 
                                        if s.get('processed_time', datetime.min).date() == date.date()])
            },
            'strategy_performances': {},
            'market_analysis': {},
            'ai_insights': {},
            'tracking_summary': {},
            'recommendations': []
        }
        
        # 策略表现汇总
        for name, perf in self.strategy_performances.items():
            report['strategy_performances'][name] = {
                'win_rate': perf.win_rate,
                'total_return': perf.total_return,
                'total_trades': perf.total_trades,
                'sharpe_ratio': perf.sharpe_ratio
            }
        
        # 跟踪策略汇总
        report['tracking_summary'] = self.strategy_tracker.get_tracker_performance()
        
        # AI洞察汇总
        if self.ai_manager:
            try:
                # 这里可以添加更多AI分析
                report['ai_insights'] = {
                    'module_status': self.ai_manager.get_module_status(),
                    'daily_analysis': '今日AI分析功能正常运行'
                }
            except Exception as e:
                report['ai_insights'] = {'error': str(e)}
        
        # 生成建议
        report['recommendations'] = self._generate_daily_recommendations()
        
        return report
    
    def _generate_daily_recommendations(self) -> List[str]:
        """生成每日建议"""
        recommendations = []
        
        # 基于持仓情况的建议
        if len(self.current_positions) > self.max_positions * 0.8:
            recommendations.append("当前持仓接近上限，建议谨慎开新仓")
        
        # 基于最近信号的建议
        recent_buy_signals = len([s for s in self.recent_signals[-20:] 
                                if s.get('action') == 'BUY'])
        recent_sell_signals = len([s for s in self.recent_signals[-20:] 
                                 if s.get('action') == 'SELL'])
        
        if recent_buy_signals > recent_sell_signals * 2:
            recommendations.append("近期买入信号较多，注意控制仓位")
        elif recent_sell_signals > recent_buy_signals * 2:
            recommendations.append("近期卖出信号较多，可能市场转弱")
        
        # 基于AI分析的建议
        if self.ai_manager:
            recommendations.append("建议结合AI分析结果进行决策")
        
        return recommendations
    
    def export_strategy_config(self) -> Dict[str, Any]:
        """导出策略配置"""
        
        config = {
            'changlun_strategy': {
                'enabled': True,
                'parameters': {
                    'min_k_for_stroke': self.changlun_strategy.min_k_for_stroke,
                    'fractal_threshold': self.changlun_strategy.fractal_threshold,
                    'base_position': self.changlun_strategy.base_position,
                    'max_position': self.changlun_strategy.max_position
                }
            },
            'ai_features': {
                'enabled': self.ai_manager is not None,
                'modules': self.ai_manager.get_module_status() if self.ai_manager else {}
            },
            'strategy_tracking': {
                'enabled': True,
                'tracked_traders': len(self.strategy_tracker.tracked_traders),
                'total_trades_tracked': sum(len(trades) for trades in self.strategy_tracker.trading_records.values())
            },
            'risk_management': {
                'max_positions': self.max_positions,
                'total_capital': self.total_capital
            }
        }
        
        return config
    
    def get_real_time_dashboard_data(self) -> Dict[str, Any]:
        """获取实时仪表板数据"""
        
        dashboard_data = {
            'timestamp': datetime.now(),
            'market_status': 'OPEN',  # 这里应该接入真实的市场状态
            'current_positions': len(self.current_positions),
            'recent_signals': self.recent_signals[-10:],  # 最近10个信号
            'strategy_status': {
                'changlun': 'ACTIVE',
                'ai_enhanced': 'ACTIVE' if self.ai_manager else 'DISABLED',
                'tracking': 'ACTIVE' if self.strategy_tracker.tracked_traders else 'DISABLED'
            },
            'performance_summary': {
                name: {
                    'win_rate': perf.win_rate,
                    'total_return': perf.total_return
                } for name, perf in self.strategy_performances.items()
            },
            'alerts': self._get_current_alerts()
        }
        
        return dashboard_data
    
    def _get_current_alerts(self) -> List[Dict[str, Any]]:
        """获取当前警报"""
        alerts = []
        
        # 检查极端RSI值
        for symbol, position in self.current_positions.items():
            # 这里应该获取实时RSI数据
            # 简化实现
            alerts.append({
                'type': 'INFO',
                'message': f'{symbol} 持仓正常',
                'timestamp': datetime.now()
            })
        
        return alerts