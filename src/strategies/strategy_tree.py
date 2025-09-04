"""
策略树 - 多策略信号融合与决策
"""
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy, TradingSignal, SignalType, SignalStrength

class StrategyTree:
    """策略决策树"""
    
    def __init__(self):
        self.strategies: List[BaseStrategy] = []
        self.signal_history: List[Dict] = []
        self.risk_threshold = 0.6  # 风险阈值
        
    def add_strategy(self, strategy: BaseStrategy):
        """添加策略"""
        self.strategies.append(strategy)
        
    def remove_strategy(self, strategy_name: str):
        """移除策略"""
        self.strategies = [s for s in self.strategies if s.name != strategy_name]
        
    def calculate_composite_signal(self, data: pd.DataFrame) -> Optional[TradingSignal]:
        """
        计算综合信号
        使用加权投票机制融合多个策略信号
        """
        if not self.strategies:
            return None
            
        signals = []
        total_weight = 0
        
        # 收集所有策略信号
        for strategy in self.strategies:
            if not strategy.enabled:
                continue
                
            signal = strategy.calculate_signal(data)
            if signal:
                signals.append((signal, strategy.weight))
                total_weight += strategy.weight
                
        if not signals:
            return None
            
        # 加权计算综合信号
        buy_score = 0
        sell_score = 0
        confidence_sum = 0
        reasons = []
        
        for signal, weight in signals:
            weighted_confidence = signal.confidence * weight
            
            if signal.signal_type == SignalType.BUY:
                buy_score += weighted_confidence * signal.strength.value
            elif signal.signal_type == SignalType.SELL:
                sell_score += weighted_confidence * signal.strength.value
                
            confidence_sum += weighted_confidence
            reasons.append(f"{signal.reason}(权重:{weight:.2f})")
            
        # 归一化分数
        if total_weight > 0:
            buy_score /= total_weight
            sell_score /= total_weight
            confidence_sum /= total_weight
            
        # 决策逻辑
        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        
        if buy_score > sell_score and buy_score > self.risk_threshold:
            signal_type = SignalType.BUY
            if buy_score > 0.8:
                strength = SignalStrength.STRONG
            elif buy_score > 0.7:
                strength = SignalStrength.MEDIUM
                
        elif sell_score > buy_score and sell_score > self.risk_threshold:
            signal_type = SignalType.SELL
            if sell_score > 0.8:
                strength = SignalStrength.STRONG
            elif sell_score > 0.7:
                strength = SignalStrength.MEDIUM
                
        if signal_type == SignalType.HOLD:
            return None
            
        composite_signal = TradingSignal(
            signal_type=signal_type,
            strength=strength,
            confidence=confidence_sum,
            reason=f"综合信号: {'; '.join(reasons)}",
            timestamp=pd.Timestamp.now()
        )
        
        # 记录信号历史
        self.signal_history.append({
            'timestamp': composite_signal.timestamp,
            'signal_type': signal_type.name,
            'strength': strength.name,
            'confidence': confidence_sum,
            'buy_score': buy_score,
            'sell_score': sell_score
        })
        
        return composite_signal
    
    def optimize_weights(self):
        """
        根据策略表现优化权重
        表现好的策略增加权重，表现差的减少权重
        """
        for strategy in self.strategies:
            win_rate = strategy.get_win_rate()
            
            if win_rate > 0.6:  # 胜率超过60%
                strategy.adjust_weight(1.1)  # 增加10%权重
            elif win_rate < 0.4:  # 胜率低于40%
                strategy.adjust_weight(0.9)  # 减少10%权重
                
    def get_strategy_performance(self) -> Dict:
        """获取所有策略表现统计"""
        performance = {}
        for strategy in self.strategies:
            performance[strategy.name] = {
                'weight': strategy.weight,
                'enabled': strategy.enabled,
                'metrics': strategy.performance_metrics
            }
        return performance