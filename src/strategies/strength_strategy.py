"""
强弱策略 - 基于相对强弱和动量的交易策略
"""
import pandas as pd
import numpy as np
from typing import Optional, List
from .base_strategy import BaseStrategy, TradingSignal, SignalType, SignalStrength

class StrengthStrategy(BaseStrategy):
    """强弱分析策略"""
    
    def __init__(self, rsi_period: int = 14, momentum_period: int = 10):
        super().__init__("强弱策略")
        self.rsi_period = rsi_period
        self.momentum_period = momentum_period
        
    def get_required_indicators(self) -> List[str]:
        return ['RSI', 'CCI', 'Williams_R', 'ROC', 'Volume_Ratio']
    
    def calculate_signal(self, data: pd.DataFrame) -> Optional[TradingSignal]:
        """
        强弱信号计算逻辑：
        1. RSI超买超卖判断
        2. CCI强弱确认
        3. Williams %R动量
        4. ROC变化率
        5. 成交量确认
        """
        if len(data) < self.momentum_period:
            return None
            
        latest = data.iloc[-1]
        
        # 1. RSI分析
        rsi_score = self._calculate_rsi_score(latest)
        
        # 2. CCI分析
        cci_score = self._calculate_cci_score(latest)
        
        # 3. Williams %R分析
        wr_score = self._calculate_williams_score(latest)
        
        # 4. ROC动量分析
        roc_score = self._calculate_roc_score(data)
        
        # 5. 成交量确认
        volume_score = self._calculate_volume_score(latest)
        
        # 综合评分 (加权平均)
        weights = [0.3, 0.2, 0.2, 0.2, 0.1]  # RSI权重最高
        scores = [rsi_score, cci_score, wr_score, roc_score, volume_score]
        
        total_score = sum(w * s for w, s in zip(weights, scores))
        confidence = min(abs(total_score), 1.0)
        
        # 信号判断
        if total_score > 0.6:
            signal_type = SignalType.BUY
            strength = SignalStrength.STRONG if total_score > 0.8 else SignalStrength.MEDIUM
            reason = f"强势信号: RSI({rsi_score:.2f}) CCI({cci_score:.2f}) WR({wr_score:.2f}) ROC({roc_score:.2f})"
            
        elif total_score < -0.6:
            signal_type = SignalType.SELL  
            strength = SignalStrength.STRONG if total_score < -0.8 else SignalStrength.MEDIUM
            reason = f"弱势信号: RSI({rsi_score:.2f}) CCI({cci_score:.2f}) WR({wr_score:.2f}) ROC({roc_score:.2f})"
            
        else:
            return None  # 强弱不明确
            
        return TradingSignal(
            signal_type=signal_type,
            strength=strength,
            confidence=confidence,
            reason=reason,
            timestamp=pd.Timestamp.now()
        )
    
    def _calculate_rsi_score(self, latest_data: pd.Series) -> float:
        """计算RSI得分"""
        rsi = latest_data.get('RSI', 50)
        
        if rsi > 80:
            return -1.0  # 超买，看空
        elif rsi > 70:
            return -0.5  # 偏强，谨慎
        elif rsi < 20:
            return 1.0   # 超卖，看多
        elif rsi < 30:
            return 0.5   # 偏弱，关注
        elif rsi > 50:
            return 0.2   # 略强
        else:
            return -0.2  # 略弱
    
    def _calculate_cci_score(self, latest_data: pd.Series) -> float:
        """计算CCI得分"""
        cci = latest_data.get('CCI', 0)
        
        if cci > 200:
            return -0.8  # 极度超买
        elif cci > 100:
            return -0.4  # 超买
        elif cci < -200:
            return 0.8   # 极度超卖
        elif cci < -100:
            return 0.4   # 超卖
        else:
            return cci / 200  # 正常范围内线性映射
    
    def _calculate_williams_score(self, latest_data: pd.Series) -> float:
        """计算Williams %R得分"""
        wr = latest_data.get('Williams_R', -50)
        
        if wr > -20:
            return -1.0  # 超买
        elif wr > -40:
            return -0.3  # 偏强
        elif wr < -80:
            return 1.0   # 超卖
        elif wr < -60:
            return 0.3   # 偏弱
        else:
            return 0     # 中性
    
    def _calculate_roc_score(self, data: pd.DataFrame) -> float:
        """计算ROC变化率得分"""
        if len(data) < self.momentum_period:
            return 0
            
        latest = data.iloc[-1]
        roc = latest.get('ROC', 0)
        
        # ROC正值表示上涨动量，负值表示下跌动量
        if roc > 10:
            return 1.0
        elif roc > 5:
            return 0.5
        elif roc < -10:
            return -1.0
        elif roc < -5:
            return -0.5
        else:
            return roc / 10  # 线性映射
    
    def _calculate_volume_score(self, latest_data: pd.Series) -> float:
        """计算成交量确认得分"""
        volume_ratio = latest_data.get('Volume_Ratio', 1.0)
        
        # 成交量放大确认信号强度
        if volume_ratio > 2.0:
            return 0.8   # 大幅放量
        elif volume_ratio > 1.5:
            return 0.5   # 适度放量
        elif volume_ratio < 0.5:
            return -0.3  # 缩量
        else:
            return 0.2   # 正常量能