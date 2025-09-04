"""
趋势策略 - 基于多重趋势确认的交易策略
"""
import pandas as pd
import numpy as np
from typing import Optional, List
from .base_strategy import BaseStrategy, TradingSignal, SignalType, SignalStrength

class TrendStrategy(BaseStrategy):
    """趋势跟踪策略"""
    
    def __init__(self, ma_periods: List[int] = [5, 20, 60]):
        super().__init__("趋势策略")
        self.ma_periods = ma_periods
        
    def get_required_indicators(self) -> List[str]:
        return [f'MA_{period}' for period in self.ma_periods] + ['ADX', 'MACD']
    
    def calculate_signal(self, data: pd.DataFrame) -> Optional[TradingSignal]:
        """
        趋势信号计算逻辑：
        1. 均线排列：短期>中期>长期 = 多头趋势
        2. ADX > 25 确认趋势强度
        3. MACD金叉/死叉确认
        """
        if len(data) < max(self.ma_periods):
            return None
            
        latest = data.iloc[-1]
        
        # 1. 均线趋势判断
        ma_trend_score = self._calculate_ma_trend(data)
        
        # 2. ADX趋势强度
        adx_strength = self._calculate_adx_strength(latest)
        
        # 3. MACD确认
        macd_signal = self._calculate_macd_signal(data)
        
        # 综合评分
        total_score = ma_trend_score + adx_strength + macd_signal
        confidence = min(abs(total_score) / 3.0, 1.0)
        
        # 信号判断
        if total_score > 2:
            signal_type = SignalType.BUY
            strength = SignalStrength.STRONG if total_score > 2.5 else SignalStrength.MEDIUM
            reason = f"多头趋势确认: MA排列({ma_trend_score:.1f}) + ADX强度({adx_strength:.1f}) + MACD({macd_signal:.1f})"\
            
        elif total_score < -2:
            signal_type = SignalType.SELL
            strength = SignalStrength.STRONG if total_score < -2.5 else SignalStrength.MEDIUM
            reason = f"空头趋势确认: MA排列({ma_trend_score:.1f}) + ADX强度({adx_strength:.1f}) + MACD({macd_signal:.1f})"\
            
        else:
            return None  # 趋势不明确
            
        return TradingSignal(
            signal_type=signal_type,
            strength=strength,
            confidence=confidence,
            reason=reason,
            timestamp=pd.Timestamp.now()
        )
    
    def _calculate_ma_trend(self, data: pd.DataFrame) -> float:
        """计算均线趋势得分"""
        latest = data.iloc[-1]
        
        # 获取各周期均线值
        ma_values = [latest[f'MA_{period}'] for period in self.ma_periods]
        
        # 检查均线排列
        if all(ma_values[i] > ma_values[i+1] for i in range(len(ma_values)-1)):
            # 多头排列
            return 1.0
        elif all(ma_values[i] < ma_values[i+1] for i in range(len(ma_values)-1)):
            # 空头排列  
            return -1.0
        else:
            # 混乱排列，计算部分得分
            score = 0
            for i in range(len(ma_values)-1):
                if ma_values[i] > ma_values[i+1]:
                    score += 0.3
                else:
                    score -= 0.3
            return score
    
    def _calculate_adx_strength(self, latest_data: pd.Series) -> float:
        """计算ADX趋势强度得分"""
        adx = latest_data.get('ADX', 0)
        
        if adx > 40:
            return 1.0  # 强趋势
        elif adx > 25:
            return 0.5  # 中等趋势
        else:
            return 0.0  # 弱趋势或震荡
    
    def _calculate_macd_signal(self, data: pd.DataFrame) -> float:
        """计算MACD信号得分"""
        if len(data) < 2:
            return 0
            
        current = data.iloc[-1]
        previous = data.iloc[-2]
        
        macd = current.get('MACD', 0)
        macd_signal = current.get('MACD_Signal', 0)
        prev_macd = previous.get('MACD', 0)
        prev_signal = previous.get('MACD_Signal', 0)
        
        # 金叉
        if macd > macd_signal and prev_macd <= prev_signal:
            return 1.0
        # 死叉
        elif macd < macd_signal and prev_macd >= prev_signal:
            return -1.0
        # 持续多头
        elif macd > macd_signal and macd > 0:
            return 0.5
        # 持续空头
        elif macd < macd_signal and macd < 0:
            return -0.5
        else:
            return 0