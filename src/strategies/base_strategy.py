"""
策略基类 - 所有策略的基础框架
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import pandas as pd
from enum import Enum

class SignalType(Enum):
    """信号类型"""
    BUY = 1
    SELL = -1
    HOLD = 0

class SignalStrength(Enum):
    """信号强度"""
    WEAK = 1
    MEDIUM = 2
    STRONG = 3

class TradingSignal:
    """交易信号"""
    def __init__(self, signal_type: SignalType, strength: SignalStrength, 
                 confidence: float, reason: str, timestamp: pd.Timestamp):
        self.signal_type = signal_type
        self.strength = strength
        self.confidence = confidence  # 0-1之间的置信度
        self.reason = reason
        self.timestamp = timestamp

class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight  # 策略权重
        self.enabled = True
        self.performance_metrics = {}
        
    @abstractmethod
    def calculate_signal(self, data: pd.DataFrame) -> Optional[TradingSignal]:
        """
        计算交易信号
        Args:
            data: 包含OHLCV数据的DataFrame
        Returns:
            TradingSignal或None
        """
        pass
    
    @abstractmethod
    def get_required_indicators(self) -> List[str]:
        """返回策略需要的技术指标列表"""
        pass
    
    def update_performance(self, profit_loss: float):
        """更新策略表现"""
        if 'total_pnl' not in self.performance_metrics:
            self.performance_metrics['total_pnl'] = 0
            self.performance_metrics['trade_count'] = 0
            
        self.performance_metrics['total_pnl'] += profit_loss
        self.performance_metrics['trade_count'] += 1
        
    def get_win_rate(self) -> float:
        """获取胜率"""
        return self.performance_metrics.get('win_rate', 0.0)
    
    def adjust_weight(self, performance_factor: float):
        """根据表现调整权重"""
        self.weight *= performance_factor
        self.weight = max(0.1, min(2.0, self.weight))  # 限制权重范围