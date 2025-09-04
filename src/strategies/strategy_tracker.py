"""
策略跟踪复制模块 - 跟踪和复制其他交易者的策略
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class TrackingMode(Enum):
    """跟踪模式"""
    REAL_TIME = "实时跟踪"
    DELAYED = "延迟跟踪"
    ANALYSIS_ONLY = "仅分析"

@dataclass
class TrackedTrader:
    """被跟踪的交易者"""
    trader_id: str
    name: str
    platform: str  # 平台来源
    win_rate: float
    total_return: float
    max_drawdown: float
    tracking_start_date: datetime
    is_active: bool = True

class StrategyTracker:
    """策略跟踪器"""
    
    def __init__(self):
        self.tracked_traders: Dict[str, TrackedTrader] = {}
        self.trading_records: Dict[str, List[Dict]] = {}  # 每个交易者的交易记录
        self.analysis_results: Dict[str, Dict] = {}
        
    def add_trader_to_track(self, trader: TrackedTrader):
        """添加要跟踪的交易者"""
        self.tracked_traders[trader.trader_id] = trader
        self.trading_records[trader.trader_id] = []
        print(f"开始跟踪交易者: {trader.name} ({trader.trader_id})")
    
    def update_trader_trades(self, trader_id: str, trades: List[Dict]):
        """更新交易者的交易记录"""
        if trader_id not in self.tracked_traders:
            print(f"交易者 {trader_id} 未在跟踪列表中")
            return
        
        # 添加新的交易记录
        for trade in trades:
            trade['timestamp'] = pd.Timestamp.now()
            trade['trader_id'] = trader_id
            
        self.trading_records[trader_id].extend(trades)
        
        # 分析交易模式
        self._analyze_trader_pattern(trader_id)
    
    def _analyze_trader_pattern(self, trader_id: str):
        """分析交易者的交易模式"""
        trades = self.trading_records[trader_id]
        if len(trades) < 10:  # 需要足够的交易样本
            return
        
        df = pd.DataFrame(trades)
        
        # 1. 交易频率分析
        trading_frequency = self._analyze_trading_frequency(df)
        
        # 2. 持仓时间分析
        holding_period = self._analyze_holding_period(df)
        
        # 3. 选股偏好分析
        stock_preference = self._analyze_stock_preference(df)
        
        # 4. 买卖时机分析
        timing_analysis = self._analyze_timing_patterns(df)
        
        # 5. 风险管理分析
        risk_management = self._analyze_risk_management(df)
        
        # 6. 盈利模式分析
        profit_pattern = self._analyze_profit_pattern(df)
        
        self.analysis_results[trader_id] = {
            'trading_frequency': trading_frequency,
            'holding_period': holding_period,
            'stock_preference': stock_preference,
            'timing_analysis': timing_analysis,
            'risk_management': risk_management,
            'profit_pattern': profit_pattern,
            'last_analysis': datetime.now()
        }
    
    def _analyze_trading_frequency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析交易频率"""
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_trades = df.groupby('date').size()
        
        return {
            'avg_daily_trades': daily_trades.mean(),
            'max_daily_trades': daily_trades.max(),
            'trading_days': len(daily_trades),
            'total_trades': len(df)
        }
    
    def _analyze_holding_period(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析持仓时间"""
        if 'entry_time' not in df.columns or 'exit_time' not in df.columns:
            return {'error': '缺少入场和出场时间数据'}
        
        df['holding_hours'] = (pd.to_datetime(df['exit_time']) - 
                              pd.to_datetime(df['entry_time'])).dt.total_seconds() / 3600
        
        return {
            'avg_holding_hours': df['holding_hours'].mean(),
            'median_holding_hours': df['holding_hours'].median(),
            'short_term_ratio': (df['holding_hours'] < 24).mean(),  # 日内交易比例
            'swing_trade_ratio': ((df['holding_hours'] >= 24) & 
                                 (df['holding_hours'] <= 168)).mean()  # 1-7天
        }
    
    def _analyze_stock_preference(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析选股偏好"""
        if 'symbol' not in df.columns:
            return {'error': '缺少股票代码数据'}
        
        stock_counts = df['symbol'].value_counts()
        
        # 分析板块偏好（需要股票板块数据）
        sector_preference = self._get_sector_preference(df['symbol'].unique())
        
        return {
            'most_traded_stocks': stock_counts.head(10).to_dict(),
            'unique_stocks_count': len(stock_counts),
            'concentration_ratio': stock_counts.head(5).sum() / len(df),  # 前5只股票占比
            'sector_preference': sector_preference
        }
    
    def _get_sector_preference(self, symbols: List[str]) -> Dict[str, int]:
        """获取板块偏好（简化版）"""
        # 这里应该接入真实的股票板块数据
        # 简化实现：根据股票代码前缀判断
        sector_map = {
            '000': '深市主板',
            '002': '中小板',
            '300': '创业板',
            '600': '沪市主板',
            '688': '科创板'
        }
        
        sector_counts = {}
        for symbol in symbols:
            prefix = symbol[:3]
            sector = sector_map.get(prefix, '其他')
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
        
        return sector_counts
    
    def _analyze_timing_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析买卖时机模式"""
        if 'entry_time' not in df.columns:
            return {'error': '缺少入场时间数据'}
        
        df['entry_hour'] = pd.to_datetime(df['entry_time']).dt.hour
        df['entry_weekday'] = pd.to_datetime(df['entry_time']).dt.weekday
        
        return {
            'preferred_entry_hours': df['entry_hour'].value_counts().head(5).to_dict(),
            'preferred_weekdays': df['entry_weekday'].value_counts().to_dict(),
            'morning_trades_ratio': (df['entry_hour'] < 12).mean(),
            'afternoon_trades_ratio': (df['entry_hour'] >= 12).mean()
        }
    
    def _analyze_risk_management(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析风险管理模式"""
        if 'profit_loss_ratio' not in df.columns:
            return {'error': '缺少盈亏数据'}
        
        profitable_trades = df[df['profit_loss_ratio'] > 0]
        losing_trades = df[df['profit_loss_ratio'] < 0]
        
        return {
            'win_rate': len(profitable_trades) / len(df),
            'avg_profit': profitable_trades['profit_loss_ratio'].mean() if len(profitable_trades) > 0 else 0,
            'avg_loss': losing_trades['profit_loss_ratio'].mean() if len(losing_trades) > 0 else 0,
            'profit_loss_ratio': (profitable_trades['profit_loss_ratio'].mean() / 
                                 abs(losing_trades['profit_loss_ratio'].mean()) 
                                 if len(losing_trades) > 0 and len(profitable_trades) > 0 else 0),
            'max_single_loss': df['profit_loss_ratio'].min(),
            'max_single_profit': df['profit_loss_ratio'].max()
        }
    
    def _analyze_profit_pattern(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析盈利模式"""
        if 'profit_loss_ratio' not in df.columns:
            return {'error': '缺少盈亏数据'}
        
        # 计算连续盈利/亏损
        df['is_profit'] = df['profit_loss_ratio'] > 0
        df['streak'] = (df['is_profit'] != df['is_profit'].shift()).cumsum()
        
        streaks = df.groupby('streak').agg({
            'is_profit': 'first',
            'profit_loss_ratio': ['count', 'sum']
        }).reset_index()
        
        profit_streaks = streaks[streaks['is_profit'] == True]['profit_loss_ratio']['count']
        loss_streaks = streaks[streaks['is_profit'] == False]['profit_loss_ratio']['count']
        
        return {
            'max_consecutive_wins': profit_streaks.max() if len(profit_streaks) > 0 else 0,
            'max_consecutive_losses': loss_streaks.max() if len(loss_streaks) > 0 else 0,
            'avg_consecutive_wins': profit_streaks.mean() if len(profit_streaks) > 0 else 0,
            'avg_consecutive_losses': loss_streaks.mean() if len(loss_streaks) > 0 else 0,
            'total_return': df['profit_loss_ratio'].sum(),
            'sharpe_ratio': df['profit_loss_ratio'].mean() / df['profit_loss_ratio'].std() if df['profit_loss_ratio'].std() > 0 else 0
        }
    
    def generate_copycat_strategy(self, trader_id: str) -> Dict[str, Any]:
        """生成模仿策略"""
        if trader_id not in self.analysis_results:
            return {'error': '该交易者分析数据不足'}
        
        analysis = self.analysis_results[trader_id]
        trader = self.tracked_traders[trader_id]
        
        # 基于分析结果生成策略规则
        strategy_rules = {
            'trader_info': {
                'name': trader.name,
                'win_rate': trader.win_rate,
                'total_return': trader.total_return
            },
            'trading_frequency': {
                'target_daily_trades': analysis['trading_frequency']['avg_daily_trades'],
                'max_daily_trades': analysis['trading_frequency']['max_daily_trades']
            },
            'position_management': {
                'avg_holding_period': analysis['holding_period']['avg_holding_hours'],
                'prefer_short_term': analysis['holding_period']['short_term_ratio'] > 0.5
            },
            'stock_selection': {
                'preferred_sectors': analysis['stock_preference']['sector_preference'],
                'concentration_limit': analysis['stock_preference']['concentration_ratio']
            },
            'timing_rules': {
                'preferred_entry_hours': analysis['timing_analysis']['preferred_entry_hours'],
                'avoid_morning_rush': analysis['timing_analysis']['morning_trades_ratio'] < 0.3
            },
            'risk_management': {
                'target_win_rate': analysis['risk_management']['win_rate'],
                'profit_loss_ratio': analysis['risk_management']['profit_loss_ratio'],
                'max_single_loss_limit': abs(analysis['risk_management']['max_single_loss']) * 0.8
            }
        }
        
        return strategy_rules
    
    def get_real_time_signals(self, trader_id: str, mode: TrackingMode = TrackingMode.DELAYED) -> List[Dict]:
        """获取实时跟单信号"""
        if trader_id not in self.tracked_traders:
            return []
        
        recent_trades = self.trading_records[trader_id][-10:]  # 最近10笔交易
        
        signals = []
        for trade in recent_trades:
            if mode == TrackingMode.REAL_TIME:
                delay_minutes = 0
            elif mode == TrackingMode.DELAYED:
                delay_minutes = 5  # 延迟5分钟
            else:
                continue  # 仅分析模式不生成信号
            
            signal = {
                'trader_id': trader_id,
                'symbol': trade.get('symbol'),
                'action': trade.get('action'),
                'price': trade.get('price'),
                'quantity': trade.get('quantity'),
                'confidence': self._calculate_signal_confidence(trader_id, trade),
                'delay_minutes': delay_minutes,
                'original_time': trade.get('timestamp'),
                'signal_time': pd.Timestamp.now() + timedelta(minutes=delay_minutes)
            }
            signals.append(signal)
        
        return signals
    
    def _calculate_signal_confidence(self, trader_id: str, trade: Dict) -> float:
        """计算跟单信号的置信度"""
        trader = self.tracked_traders[trader_id]
        
        # 基础置信度基于交易者历史表现
        base_confidence = trader.win_rate * 0.6 + (trader.total_return / 100) * 0.2
        
        # 根据最近表现调整
        recent_trades = self.trading_records[trader_id][-20:]
        if recent_trades:
            recent_df = pd.DataFrame(recent_trades)
            if 'profit_loss_ratio' in recent_df.columns:
                recent_win_rate = (recent_df['profit_loss_ratio'] > 0).mean()
                recent_performance_factor = recent_win_rate / max(trader.win_rate, 0.01)
                base_confidence *= recent_performance_factor
        
        # 根据交易类型调整
        if trade.get('action') == 'BUY':
            # 买入信号相对保守
            confidence = base_confidence * 0.9
        else:
            # 卖出信号相对激进
            confidence = base_confidence * 1.1
        
        return min(max(confidence, 0.1), 0.95)  # 限制在0.1-0.95之间
    
    def get_tracker_performance(self) -> Dict[str, Any]:
        """获取跟踪器整体表现"""
        performance = {
            'total_tracked_traders': len(self.tracked_traders),
            'active_traders': sum(1 for t in self.tracked_traders.values() if t.is_active),
            'total_trades_tracked': sum(len(trades) for trades in self.trading_records.values()),
            'traders_performance': {}
        }
        
        for trader_id, trader in self.tracked_traders.items():
            trades_count = len(self.trading_records.get(trader_id, []))
            performance['traders_performance'][trader_id] = {
                'name': trader.name,
                'win_rate': trader.win_rate,
                'total_return': trader.total_return,
                'trades_tracked': trades_count,
                'last_analysis': self.analysis_results.get(trader_id, {}).get('last_analysis')
            }
        
        return performance
    
    def export_strategy_template(self, trader_id: str, format_type: str = 'python') -> str:
        """导出策略模板代码"""
        strategy_rules = self.generate_copycat_strategy(trader_id)
        
        if format_type == 'python':
            return self._generate_python_strategy_code(trader_id, strategy_rules)
        elif format_type == 'json':
            import json
            return json.dumps(strategy_rules, indent=2, ensure_ascii=False)
        else:
            return str(strategy_rules)
    
    def _generate_python_strategy_code(self, trader_id: str, rules: Dict) -> str:
        """生成Python策略代码"""
        trader_name = rules['trader_info']['name']
        
        code_template = f'''
"""
模仿策略: {trader_name}
基于交易者 {trader_id} 的交易模式自动生成
"""

import pandas as pd
from src.strategies.base_strategy import BaseStrategy, TradingSignal, SignalType, SignalStrength

class CopycatStrategy_{trader_id.replace('-', '_')}(BaseStrategy):
    def __init__(self):
        super().__init__("模仿策略_{trader_name}")
        
        # 基于分析的策略参数
        self.target_win_rate = {rules['risk_management']['target_win_rate']:.2f}
        self.max_daily_trades = {rules['trading_frequency']['max_daily_trades']}
        self.avg_holding_hours = {rules['position_management']['avg_holding_period']:.1f}
        self.max_single_loss = {rules['risk_management']['max_single_loss_limit']:.3f}
        
        # 偏好设置
        self.preferred_sectors = {rules['stock_selection']['preferred_sectors']}
        self.preferred_hours = {list(rules['timing_rules']['preferred_entry_hours'].keys())}
        
    def calculate_signal(self, data: pd.DataFrame) -> Optional[TradingSignal]:
        # 这里实现具体的信号逻辑
        # 基于原交易者的模式进行判断
        pass
        
    def should_enter_position(self, symbol: str, current_time: pd.Timestamp) -> bool:
        # 检查是否符合入场条件
        hour = current_time.hour
        return hour in self.preferred_hours
        
    def calculate_position_size(self, confidence: float) -> float:
        # 基于置信度和风险管理规则计算仓位
        base_size = 0.1  # 基础仓位10%
        return base_size * confidence * (self.target_win_rate / 0.5)
'''
        
        return code_template