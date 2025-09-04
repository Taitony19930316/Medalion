"""
缠论策略 - 基于日线一笔级别的完整交易体系
包含趋势、强弱、位置、背驰、情绪、仓位管理六大维度
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from enum import Enum
from .base_strategy import BaseStrategy, TradingSignal, SignalType, SignalStrength

class TrendDirection(Enum):
    """趋势方向"""
    UP = 1      # 上涨趋势
    DOWN = -1   # 下跌趋势
    SIDEWAYS = 0  # 震荡

class RelativePosition(Enum):
    """相对位置"""
    HIGH = 3    # 高位
    MEDIUM_HIGH = 2  # 中高位
    MEDIUM = 1  # 中位
    MEDIUM_LOW = 0   # 中低位
    LOW = -1    # 低位

class BuyingSellPoint(Enum):
    """买卖点类型"""
    BUY_1 = "一买"   # 第一类买点
    BUY_2 = "二买"   # 第二类买点  
    BUY_3 = "三买"   # 第三类买点
    SELL_1 = "一卖"  # 第一类卖点
    SELL_2 = "二卖"  # 第二类卖点
    SELL_3 = "三卖"  # 第三类卖点

class ChangLunStrategy(BaseStrategy):
    """缠论完整交易策略"""
    
    def __init__(self, params: Dict = None):
        super().__init__("缠论日线一笔策略")
        self.params = params or {}
        
        # 缠论参数
        self.min_k_for_stroke = 5  # 构成笔的最小K线数
        self.fractal_threshold = 0.01  # 分型识别阈值
        
        # 趋势参数
        self.trend_ma_periods = [5, 20, 60]  # 趋势判断均线
        
        # 相对位置参数
        self.position_lookback = 120  # 相对位置回看周期
        
        # 背驰参数
        self.macd_params = (12, 26, 9)  # MACD参数
        
        # 情绪指标参数
        self.rsi_period = 14
        self.rsi_overbought = 80
        self.rsi_oversold = 20
        
        # 仓位管理参数
        self.base_position = 0.2  # 基础仓位20%
        self.max_position = 0.5   # 最大仓位50%
        
    def get_required_indicators(self) -> List[str]:
        return ['MA_5', 'MA_20', 'MA_60', 'MACD', 'MACD_Signal', 'MACD_Hist', 'RSI', 'Volume']
    
    def calculate_signal(self, data: pd.DataFrame) -> Optional[TradingSignal]:
        """计算综合交易信号"""
        if len(data) < self.position_lookback:
            return None
        
        # 1. 识别笔和分型
        fractals = self._identify_fractals(data)
        strokes = self._identify_strokes(data, fractals)
        
        if not strokes:
            return None
        
        # 2. 判断趋势方向
        trend_direction = self._analyze_trend(data, strokes)
        
        # 3. 计算相对位置
        relative_position = self._calculate_relative_position(data)
        
        # 4. 识别买卖点
        buy_sell_points = self._identify_buy_sell_points(data, strokes, trend_direction)
        
        # 5. 检测背驰信号
        divergence_signal = self._detect_divergence(data, strokes)
        
        # 6. 监控情绪指标
        emotion_signal = self._monitor_emotion_indicators(data)
        
        # 7. 综合决策
        final_signal = self._make_comprehensive_decision(
            trend_direction, relative_position, buy_sell_points, 
            divergence_signal, emotion_signal, data
        )
        
        return final_signal
    
    def _identify_fractals(self, data: pd.DataFrame) -> List[Dict]:
        """识别分型"""
        fractals = []
        
        for i in range(2, len(data) - 2):
            high = data['high'].iloc[i]
            low = data['low'].iloc[i]
            
            # 顶分型：中间K线高点是局部最高
            if (high > data['high'].iloc[i-2] and high > data['high'].iloc[i-1] and
                high > data['high'].iloc[i+1] and high > data['high'].iloc[i+2]):
                fractals.append({
                    'index': i,
                    'type': 'top',
                    'price': high,
                    'timestamp': data.index[i]
                })
            
            # 底分型：中间K线低点是局部最低
            if (low < data['low'].iloc[i-2] and low < data['low'].iloc[i-1] and
                low < data['low'].iloc[i+1] and low < data['low'].iloc[i+2]):
                fractals.append({
                    'index': i,
                    'type': 'bottom',
                    'price': low,
                    'timestamp': data.index[i]
                })
        
        return fractals
    
    def _identify_strokes(self, data: pd.DataFrame, fractals: List[Dict]) -> List[Dict]:
        """识别笔"""
        if len(fractals) < 2:
            return []
        
        strokes = []
        current_fractal = fractals[0]
        
        for next_fractal in fractals[1:]:
            # 检查是否构成笔：类型不同且间隔足够
            if (current_fractal['type'] != next_fractal['type'] and
                next_fractal['index'] - current_fractal['index'] >= self.min_k_for_stroke):
                
                # 计算笔的方向和强度
                if current_fractal['type'] == 'bottom' and next_fractal['type'] == 'top':
                    direction = 'up'
                    strength = (next_fractal['price'] - current_fractal['price']) / current_fractal['price']
                else:
                    direction = 'down'
                    strength = (current_fractal['price'] - next_fractal['price']) / current_fractal['price']
                
                strokes.append({
                    'start_fractal': current_fractal,
                    'end_fractal': next_fractal,
                    'direction': direction,
                    'strength': strength,
                    'start_index': current_fractal['index'],
                    'end_index': next_fractal['index']
                })
                
                current_fractal = next_fractal
        
        return strokes
    
    def _analyze_trend(self, data: pd.DataFrame, strokes: List[Dict]) -> TrendDirection:
        """分析趋势方向"""
        if len(strokes) < 3:
            return TrendDirection.SIDEWAYS
        
        # 方法1：基于最近几笔的方向
        recent_strokes = strokes[-3:]
        up_strokes = sum(1 for stroke in recent_strokes if stroke['direction'] == 'up')
        down_strokes = sum(1 for stroke in recent_strokes if stroke['direction'] == 'down')
        
        # 方法2：基于均线排列
        latest = data.iloc[-1]
        ma5 = latest['MA_5']
        ma20 = latest['MA_20']
        ma60 = latest['MA_60']
        
        ma_trend_score = 0
        if ma5 > ma20 > ma60:
            ma_trend_score = 1  # 多头排列
        elif ma5 < ma20 < ma60:
            ma_trend_score = -1  # 空头排列
        
        # 综合判断
        stroke_trend_score = 1 if up_strokes > down_strokes else -1 if down_strokes > up_strokes else 0
        
        combined_score = (stroke_trend_score + ma_trend_score) / 2
        
        if combined_score > 0.5:
            return TrendDirection.UP
        elif combined_score < -0.5:
            return TrendDirection.DOWN
        else:
            return TrendDirection.SIDEWAYS
    
    def _calculate_relative_position(self, data: pd.DataFrame) -> RelativePosition:
        """计算当前价格的相对位置"""
        lookback_data = data.tail(self.position_lookback)
        
        current_price = data['close'].iloc[-1]
        high_price = lookback_data['high'].max()
        low_price = lookback_data['low'].min()
        
        # 计算相对位置百分比
        if high_price == low_price:
            position_pct = 0.5
        else:
            position_pct = (current_price - low_price) / (high_price - low_price)
        
        # 分类相对位置
        if position_pct >= 0.8:
            return RelativePosition.HIGH
        elif position_pct >= 0.6:
            return RelativePosition.MEDIUM_HIGH
        elif position_pct >= 0.4:
            return RelativePosition.MEDIUM
        elif position_pct >= 0.2:
            return RelativePosition.MEDIUM_LOW
        else:
            return RelativePosition.LOW
    
    def _identify_buy_sell_points(self, data: pd.DataFrame, strokes: List[Dict], 
                                 trend: TrendDirection) -> List[BuyingSellPoint]:
        """识别买卖点"""
        if len(strokes) < 2:
            return []
        
        buy_sell_points = []
        latest_stroke = strokes[-1]
        
        # 根据趋势和笔的结构判断买卖点
        if trend == TrendDirection.UP:
            if latest_stroke['direction'] == 'down':
                # 上涨趋势中的回调，可能是买点
                if len(strokes) >= 3:
                    prev_stroke = strokes[-2]
                    if prev_stroke['direction'] == 'up':
                        # 判断是二买还是三买
                        if self._is_second_buy_point(data, strokes):
                            buy_sell_points.append(BuyingSellPoint.BUY_2)
                        elif self._is_third_buy_point(data, strokes):
                            buy_sell_points.append(BuyingSellPoint.BUY_3)
        
        elif trend == TrendDirection.DOWN:
            if latest_stroke['direction'] == 'up':
                # 下跌趋势中的反弹，可能是卖点
                if len(strokes) >= 3:
                    prev_stroke = strokes[-2]
                    if prev_stroke['direction'] == 'down':
                        # 判断是二卖还是三卖
                        if self._is_second_sell_point(data, strokes):
                            buy_sell_points.append(BuyingSellPoint.SELL_2)
                        elif self._is_third_sell_point(data, strokes):
                            buy_sell_points.append(BuyingSellPoint.SELL_3)
        
        return buy_sell_points
    
    def _is_second_buy_point(self, data: pd.DataFrame, strokes: List[Dict]) -> bool:
        """判断是否为二买点"""
        # 简化判断：回调不破前低，且有支撑
        if len(strokes) < 3:
            return False
        
        current_stroke = strokes[-1]  # 当前下跌笔
        prev_up_stroke = strokes[-2]  # 前一上涨笔
        
        # 二买特征：回调幅度适中，不破关键支撑
        if current_stroke['direction'] == 'down':
            retracement = current_stroke['strength']
            return 0.3 <= retracement <= 0.618  # 黄金分割回调
        
        return False
    
    def _is_third_buy_point(self, data: pd.DataFrame, strokes: List[Dict]) -> bool:
        """判断是否为三买点"""
        # 三买：突破前高后的回调买点
        if len(strokes) < 4:
            return False
        
        # 检查是否有突破前高的走势
        recent_highs = [stroke['end_fractal']['price'] for stroke in strokes[-4:] 
                       if stroke['direction'] == 'up']
        
        if len(recent_highs) >= 2:
            return recent_highs[-1] > recent_highs[-2]  # 创新高
        
        return False
    
    def _is_second_sell_point(self, data: pd.DataFrame, strokes: List[Dict]) -> bool:
        """判断是否为二卖点"""
        # 类似二买的逻辑，但方向相反
        if len(strokes) < 3:
            return False
        
        current_stroke = strokes[-1]  # 当前上涨笔
        
        if current_stroke['direction'] == 'up':
            rebound = current_stroke['strength']
            return 0.3 <= rebound <= 0.618
        
        return False
    
    def _is_third_sell_point(self, data: pd.DataFrame, strokes: List[Dict]) -> bool:
        """判断是否为三卖点"""
        # 三卖：跌破前低后的反弹卖点
        if len(strokes) < 4:
            return False
        
        recent_lows = [stroke['end_fractal']['price'] for stroke in strokes[-4:] 
                      if stroke['direction'] == 'down']
        
        if len(recent_lows) >= 2:
            return recent_lows[-1] < recent_lows[-2]  # 创新低
        
        return False
    
    def _detect_divergence(self, data: pd.DataFrame, strokes: List[Dict]) -> Optional[str]:
        """检测背驰信号"""
        if len(strokes) < 2 or len(data) < 50:
            return None
        
        # 获取MACD数据
        macd = data['MACD'].values
        macd_hist = data['MACD_Hist'].values
        
        latest_stroke = strokes[-1]
        prev_stroke = strokes[-2] if len(strokes) >= 2 else None
        
        if not prev_stroke or latest_stroke['direction'] != prev_stroke['direction']:
            return None
        
        # 检查价格和MACD的背离
        if latest_stroke['direction'] == 'up':
            # 上涨背驰：价格创新高但MACD不创新高
            price_high1 = prev_stroke['end_fractal']['price']
            price_high2 = latest_stroke['end_fractal']['price']
            
            macd_high1 = macd[prev_stroke['end_index']]
            macd_high2 = macd[latest_stroke['end_index']]
            
            if price_high2 > price_high1 and macd_high2 < macd_high1:
                return 'bullish_divergence'  # 顶背驰
        
        elif latest_stroke['direction'] == 'down':
            # 下跌背驰：价格创新低但MACD不创新低
            price_low1 = prev_stroke['end_fractal']['price']
            price_low2 = latest_stroke['end_fractal']['price']
            
            macd_low1 = macd[prev_stroke['end_index']]
            macd_low2 = macd[latest_stroke['end_index']]
            
            if price_low2 < price_low1 and macd_low2 > macd_low1:
                return 'bearish_divergence'  # 底背驰
        
        return None
    
    def _monitor_emotion_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """监控情绪指标"""
        latest = data.iloc[-1]
        rsi = latest['RSI']
        
        emotion_signals = {
            'rsi_overbought': rsi > self.rsi_overbought,
            'rsi_oversold': rsi < self.rsi_oversold,
            'extreme_emotion': rsi > 90 or rsi < 10,
            'rsi_value': rsi
        }
        
        # 可以添加更多情绪指标
        # 如恐慌指数、换手率等
        
        return emotion_signals
    
    def _make_comprehensive_decision(self, trend: TrendDirection, position: RelativePosition,
                                   buy_sell_points: List[BuyingSellPoint], 
                                   divergence: Optional[str], emotion: Dict[str, Any],
                                   data: pd.DataFrame) -> Optional[TradingSignal]:
        """综合决策"""
        
        signal_type = SignalType.HOLD
        strength = SignalStrength.WEAK
        confidence = 0.5
        reasons = []
        
        # 1. 趋势一致性检查
        if trend == TrendDirection.UP and any(bp in [BuyingSellPoint.BUY_2, BuyingSellPoint.BUY_3] 
                                             for bp in buy_sell_points):
            signal_type = SignalType.BUY
            reasons.append(f"趋势向上且出现{[bp.value for bp in buy_sell_points]}")
            confidence += 0.2
        
        elif trend == TrendDirection.DOWN and any(bp in [BuyingSellPoint.SELL_2, BuyingSellPoint.SELL_3] 
                                                 for bp in buy_sell_points):
            signal_type = SignalType.SELL
            reasons.append(f"趋势向下且出现{[bp.value for bp in buy_sell_points]}")
            confidence += 0.2
        
        # 2. 相对位置加权
        if signal_type == SignalType.BUY:
            if position in [RelativePosition.LOW, RelativePosition.MEDIUM_LOW]:
                confidence += 0.2
                reasons.append("相对位置较低，安全边际高")
            elif position == RelativePosition.HIGH:
                confidence -= 0.1
                reasons.append("相对位置较高，需谨慎")
        
        elif signal_type == SignalType.SELL:
            if position in [RelativePosition.HIGH, RelativePosition.MEDIUM_HIGH]:
                confidence += 0.2
                reasons.append("相对位置较高，获利空间有限")
        
        # 3. 背驰信号确认
        if divergence:
            if divergence == 'bearish_divergence' and signal_type == SignalType.BUY:
                confidence += 0.15
                reasons.append("底背驰确认买入信号")
            elif divergence == 'bullish_divergence' and signal_type == SignalType.SELL:
                confidence += 0.15
                reasons.append("顶背驰确认卖出信号")
        
        # 4. 情绪指标过滤
        if emotion['extreme_emotion']:
            if emotion['rsi_oversold'] and signal_type == SignalType.BUY:
                confidence += 0.1
                strength = SignalStrength.STRONG
                reasons.append(f"RSI极度超卖({emotion['rsi_value']:.1f})，情绪极端")
            elif emotion['rsi_overbought'] and signal_type == SignalType.SELL:
                confidence += 0.1
                strength = SignalStrength.STRONG
                reasons.append(f"RSI极度超买({emotion['rsi_value']:.1f})，情绪极端")
        
        # 5. 信号强度判断
        if confidence >= 0.8:
            strength = SignalStrength.STRONG
        elif confidence >= 0.6:
            strength = SignalStrength.MEDIUM
        
        # 6. 最终过滤
        if signal_type == SignalType.HOLD or confidence < 0.5:
            return None
        
        return TradingSignal(
            signal_type=signal_type,
            strength=strength,
            confidence=min(confidence, 1.0),
            reason=f"缠论综合信号: {'; '.join(reasons)}",
            timestamp=pd.Timestamp.now()
        )
    
    def calculate_position_size(self, signal: TradingSignal, market_data: pd.DataFrame) -> float:
        """计算仓位大小"""
        base_size = self.base_position
        
        # 根据信号强度调整
        if signal.strength == SignalStrength.STRONG:
            size_multiplier = 1.5
        elif signal.strength == SignalStrength.MEDIUM:
            size_multiplier = 1.2
        else:
            size_multiplier = 1.0
        
        # 根据置信度调整
        confidence_multiplier = signal.confidence
        
        # 根据相对位置调整
        position = self._calculate_relative_position(market_data)
        if signal.signal_type == SignalType.BUY:
            if position == RelativePosition.LOW:
                position_multiplier = 1.3
            elif position == RelativePosition.HIGH:
                position_multiplier = 0.7
            else:
                position_multiplier = 1.0
        else:
            position_multiplier = 1.0
        
        final_size = base_size * size_multiplier * confidence_multiplier * position_multiplier
        
        return min(final_size, self.max_position)
    
    def get_strategy_status(self, data: pd.DataFrame) -> Dict[str, Any]:
        """获取策略当前状态"""
        if len(data) < 50:
            return {'status': 'insufficient_data'}
        
        # 计算各个维度的状态
        fractals = self._identify_fractals(data)
        strokes = self._identify_strokes(data, fractals)
        trend = self._analyze_trend(data, strokes)
        position = self._calculate_relative_position(data)
        divergence = self._detect_divergence(data, strokes)
        emotion = self._monitor_emotion_indicators(data)
        
        return {
            'trend_direction': trend.name,
            'relative_position': position.name,
            'recent_strokes_count': len(strokes),
            'divergence_signal': divergence,
            'rsi_value': emotion['rsi_value'],
            'emotion_extreme': emotion['extreme_emotion'],
            'last_fractal': fractals[-1] if fractals else None,
            'last_stroke': strokes[-1] if strokes else None
        }