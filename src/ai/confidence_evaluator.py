"""
置信度评估器 - 实时评估市场对策略的适配度
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .base_ai_module import BaseAIModule

class ConfidenceEvaluator(BaseAIModule):
    """策略置信度评估器"""
    
    def __init__(self, model_config: Dict[str, Any]):
        super().__init__(model_config)
        self.evaluation_history = []
        
    def evaluate_strategy_confidence(self, 
                                   strategy_name: str,
                                   market_data: Dict[str, pd.DataFrame],
                                   recent_signals: pd.DataFrame,
                                   market_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """评估策略在当前市场环境下的置信度"""
        
        # 1. 技术面置信度评估
        technical_confidence = self._evaluate_technical_confidence(market_data, recent_signals)
        
        # 2. 市场环境适配度评估
        market_fit_confidence = self._evaluate_market_fit(market_indicators, strategy_name)
        
        # 3. 历史表现置信度
        historical_confidence = self._evaluate_historical_performance(strategy_name, recent_signals)
        
        # 4. AI综合评估
        ai_confidence = self._ai_comprehensive_evaluation(
            strategy_name, market_data, recent_signals, market_indicators
        )
        
        # 综合置信度计算
        overall_confidence = self._calculate_overall_confidence(
            technical_confidence, market_fit_confidence, historical_confidence, ai_confidence
        )
        
        evaluation_result = {
            'strategy_name': strategy_name,
            'timestamp': datetime.now(),
            'overall_confidence': overall_confidence,
            'confidence_breakdown': {
                'technical': technical_confidence,
                'market_fit': market_fit_confidence,
                'historical': historical_confidence,
                'ai_evaluation': ai_confidence
            },
            'recommendation': self._generate_recommendation(overall_confidence),
            'risk_level': self._assess_risk_level(overall_confidence, market_indicators),
            'suggested_position_size': self._suggest_position_size(overall_confidence)
        }
        
        # 保存评估历史
        self.evaluation_history.append(evaluation_result)
        
        return evaluation_result
    
    def _evaluate_technical_confidence(self, 
                                     market_data: Dict[str, pd.DataFrame],
                                     recent_signals: pd.DataFrame) -> float:
        """评估技术面置信度"""
        
        if recent_signals.empty:
            return 0.5
        
        # 计算信号质量指标
        signal_strength = 0.0
        signal_count = 0
        
        for stock, data in market_data.items():
            if len(data) < 20:
                continue
                
            # 趋势一致性
            ma5 = data['close'].rolling(5).mean()
            ma20 = data['close'].rolling(20).mean()
            trend_consistency = (ma5.iloc[-1] > ma20.iloc[-1]) * 0.3
            
            # 成交量确认
            volume_confirmation = (data['volume'].iloc[-1] > data['volume'].rolling(10).mean().iloc[-1]) * 0.2
            
            # 价格动量
            momentum = data['close'].pct_change(5).iloc[-1]
            momentum_score = min(abs(momentum) * 10, 0.3)
            
            signal_strength += trend_consistency + volume_confirmation + momentum_score
            signal_count += 1
        
        return min(signal_strength / max(signal_count, 1), 1.0) if signal_count > 0 else 0.5
    
    def _evaluate_market_fit(self, market_indicators: Dict[str, Any], strategy_name: str) -> float:
        """评估市场环境适配度"""
        
        # 市场波动率
        volatility = market_indicators.get('volatility', 0.02)
        volatility_score = 1.0 - min(volatility / 0.05, 1.0)  # 波动率越低越好
        
        # 市场趋势强度
        trend_strength = market_indicators.get('trend_strength', 0.5)
        
        # 市场情绪指标
        market_sentiment = market_indicators.get('sentiment', 0.5)
        
        # 根据策略类型调整权重
        if 'trend' in strategy_name.lower():
            return trend_strength * 0.6 + volatility_score * 0.2 + market_sentiment * 0.2
        elif 'reversal' in strategy_name.lower():
            return (1 - trend_strength) * 0.6 + volatility_score * 0.2 + market_sentiment * 0.2
        else:
            return (trend_strength + volatility_score + market_sentiment) / 3
    
    def _evaluate_historical_performance(self, strategy_name: str, recent_signals: pd.DataFrame) -> float:
        """评估历史表现置信度"""
        
        # 简化实现：基于最近信号的成功率
        if len(recent_signals) < 10:
            return 0.5
        
        # 计算最近信号的成功率
        successful_signals = len(recent_signals[recent_signals['profit'] > 0])
        success_rate = successful_signals / len(recent_signals)
        
        # 考虑盈亏比
        avg_profit = recent_signals[recent_signals['profit'] > 0]['profit'].mean() if successful_signals > 0 else 0
        avg_loss = abs(recent_signals[recent_signals['profit'] < 0]['profit'].mean()) if len(recent_signals) - successful_signals > 0 else 1
        
        profit_loss_ratio = avg_profit / avg_loss if avg_loss > 0 else 1
        
        # 综合评分
        return min((success_rate * 0.7 + min(profit_loss_ratio / 2, 0.3)), 1.0)
    
    def _ai_comprehensive_evaluation(self, 
                                   strategy_name: str,
                                   market_data: Dict[str, pd.DataFrame],
                                   recent_signals: pd.DataFrame,
                                   market_indicators: Dict[str, Any]) -> float:
        """AI综合评估"""
        
        # 构建评估提示词
        prompt = self._build_evaluation_prompt(strategy_name, market_data, recent_signals, market_indicators)
        
        system_prompt = """你是专业的量化交易策略评估专家。
        请根据提供的市场数据和策略表现，评估该策略在当前市场环境下的置信度。
        
        请返回一个0-1之间的置信度分数，并简要说明理由。
        
        格式：
        置信度: 0.75
        理由: [简要分析]"""
        
        try:
            evaluation_result = self.call_llm(prompt, system_prompt)
            
            # 提取置信度分数
            confidence_score = self._extract_confidence_score(evaluation_result)
            
            return confidence_score
            
        except Exception as e:
            # AI评估失败时返回中性值
            return 0.5
    
    def _build_evaluation_prompt(self, 
                               strategy_name: str,
                               market_data: Dict[str, pd.DataFrame],
                               recent_signals: pd.DataFrame,
                               market_indicators: Dict[str, Any]) -> str:
        """构建评估提示词"""
        
        # 市场概况
        market_summary = self._summarize_market_data(market_data)
        
        # 策略表现摘要
        strategy_summary = self._summarize_strategy_performance(recent_signals)
        
        prompt = f"""
        请评估策略 "{strategy_name}" 在当前市场环境下的置信度：
        
        ## 当前市场环境
        {market_summary}
        
        ## 市场指标
        - 波动率: {market_indicators.get('volatility', 'N/A')}
        - 趋势强度: {market_indicators.get('trend_strength', 'N/A')}
        - 市场情绪: {market_indicators.get('sentiment', 'N/A')}
        
        ## 策略近期表现
        {strategy_summary}
        
        ## 最近信号样本
        {recent_signals.tail(5).to_string() if not recent_signals.empty else '暂无信号'}
        
        请综合考虑市场环境、策略特点和历史表现，给出置信度评估。
        """
        
        return prompt
    
    def _summarize_market_data(self, market_data: Dict[str, pd.DataFrame]) -> str:
        """总结市场数据"""
        if not market_data:
            return "市场数据不足"
        
        # 计算市场整体表现
        total_stocks = len(market_data)
        rising_stocks = 0
        
        for stock, data in market_data.items():
            if len(data) >= 5:
                recent_change = (data['close'].iloc[-1] - data['close'].iloc[-5]) / data['close'].iloc[-5]
                if recent_change > 0:
                    rising_stocks += 1
        
        rising_ratio = rising_stocks / total_stocks if total_stocks > 0 else 0
        
        return f"市场概况: {total_stocks}只股票，{rising_ratio:.1%}上涨"
    
    def _summarize_strategy_performance(self, recent_signals: pd.DataFrame) -> str:
        """总结策略表现"""
        if recent_signals.empty:
            return "暂无交易记录"
        
        total_trades = len(recent_signals)
        profitable_trades = len(recent_signals[recent_signals['profit'] > 0])
        win_rate = profitable_trades / total_trades
        avg_profit = recent_signals['profit'].mean()
        
        return f"近期表现: {total_trades}笔交易，胜率{win_rate:.1%}，平均收益{avg_profit:.2%}"
    
    def _extract_confidence_score(self, evaluation_text: str) -> float:
        """从评估文本中提取置信度分数"""
        import re
        
        # 查找置信度数值
        patterns = [
            r'置信度[：:]\s*([0-9.]+)',
            r'confidence[：:]\s*([0-9.]+)',
            r'([0-9.]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, evaluation_text, re.IGNORECASE)
            if match:
                try:
                    score = float(match.group(1))
                    return min(max(score, 0), 1)  # 确保在0-1范围内
                except ValueError:
                    continue
        
        return 0.5  # 默认值
    
    def _calculate_overall_confidence(self, 
                                    technical: float, 
                                    market_fit: float, 
                                    historical: float, 
                                    ai_eval: float) -> float:
        """计算综合置信度"""
        
        # 加权平均
        weights = {
            'technical': 0.25,
            'market_fit': 0.25,
            'historical': 0.3,
            'ai_eval': 0.2
        }
        
        overall = (technical * weights['technical'] + 
                  market_fit * weights['market_fit'] + 
                  historical * weights['historical'] + 
                  ai_eval * weights['ai_eval'])
        
        return round(overall, 3)
    
    def _generate_recommendation(self, confidence: float) -> str:
        """生成投资建议"""
        if confidence >= 0.8:
            return "强烈推荐"
        elif confidence >= 0.6:
            return "推荐"
        elif confidence >= 0.4:
            return "谨慎观望"
        else:
            return "不推荐"
    
    def _assess_risk_level(self, confidence: float, market_indicators: Dict[str, Any]) -> str:
        """评估风险等级"""
        volatility = market_indicators.get('volatility', 0.02)
        
        if confidence < 0.4 or volatility > 0.05:
            return "高风险"
        elif confidence < 0.6 or volatility > 0.03:
            return "中风险"
        else:
            return "低风险"
    
    def _suggest_position_size(self, confidence: float) -> float:
        """建议仓位大小"""
        if confidence >= 0.8:
            return 0.3  # 30%
        elif confidence >= 0.6:
            return 0.2  # 20%
        elif confidence >= 0.4:
            return 0.1  # 10%
        else:
            return 0.05  # 5%
    
    def get_confidence_trend(self, strategy_name: str, days: int = 30) -> Dict[str, Any]:
        """获取置信度趋势"""
        
        # 筛选指定策略的历史评估
        strategy_history = [
            eval_result for eval_result in self.evaluation_history
            if eval_result['strategy_name'] == strategy_name and
            eval_result['timestamp'] >= datetime.now() - timedelta(days=days)
        ]
        
        if not strategy_history:
            return {'trend': 'insufficient_data', 'message': '数据不足'}
        
        # 计算趋势
        confidences = [result['overall_confidence'] for result in strategy_history]
        
        if len(confidences) >= 2:
            trend_slope = (confidences[-1] - confidences[0]) / len(confidences)
            
            if trend_slope > 0.01:
                trend = 'improving'
            elif trend_slope < -0.01:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'current_confidence': confidences[-1] if confidences else 0,
            'avg_confidence': np.mean(confidences) if confidences else 0,
            'confidence_history': confidences
        }
    
    def process(self, 
               strategy_name: str,
               market_data: Dict[str, pd.DataFrame],
               recent_signals: pd.DataFrame,
               market_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """主要处理方法"""
        return self.evaluate_strategy_confidence(strategy_name, market_data, recent_signals, market_indicators)