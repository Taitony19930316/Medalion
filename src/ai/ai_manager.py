"""
AI管理器 - 统一管理所有AI功能模块
"""
from typing import Dict, List, Any, Optional
import pandas as pd
from config import Config
from .strategy_analyzer import StrategyAnalyzer
from .nlp_strategy_generator import NLPStrategyGenerator
from .stock_screener import AIStockScreener
from .confidence_evaluator import ConfidenceEvaluator
from loguru import logger

class AIManager:
    """AI功能管理器"""
    
    def __init__(self, model_config: Dict[str, Any] = None):
        self.model_config = model_config or Config.AI_MODEL_CONFIG
        
        # 初始化各个AI模块
        self.strategy_analyzer = None
        self.nlp_generator = None
        self.stock_screener = None
        self.confidence_evaluator = None
        
        self._initialize_modules()
    
    def _initialize_modules(self):
        """初始化AI模块"""
        try:
            if Config.ENABLE_AI_STRATEGY_ANALYSIS:
                self.strategy_analyzer = StrategyAnalyzer(self.model_config)
                logger.info("策略分析器初始化成功")
            
            if Config.ENABLE_NLP_STRATEGY_GENERATION:
                self.nlp_generator = NLPStrategyGenerator(self.model_config)
                logger.info("NLP策略生成器初始化成功")
            
            if Config.ENABLE_AI_STOCK_SCREENING:
                self.stock_screener = AIStockScreener(self.model_config)
                logger.info("AI股票筛选器初始化成功")
            
            if Config.ENABLE_AI_CONFIDENCE_EVALUATION:
                self.confidence_evaluator = ConfidenceEvaluator(self.model_config)
                logger.info("置信度评估器初始化成功")
                
        except Exception as e:
            logger.error(f"AI模块初始化失败: {e}")
    
    def analyze_trading_history(self, trades_df: pd.DataFrame) -> Dict[str, Any]:
        """分析交易历史"""
        if not self.strategy_analyzer:
            return {'error': '策略分析器未启用'}
        
        try:
            return self.strategy_analyzer.process(trades_df)
        except Exception as e:
            logger.error(f"交易历史分析失败: {e}")
            return {'error': str(e)}
    
    def generate_strategy_from_description(self, description: str) -> Dict[str, Any]:
        """根据描述生成策略"""
        if not self.nlp_generator:
            return {'error': 'NLP策略生成器未启用'}
        
        try:
            return self.nlp_generator.process(description)
        except Exception as e:
            logger.error(f"策略生成失败: {e}")
            return {'error': str(e)}
    
    def screen_stocks_intelligently(self, 
                                  stock_pool: List[str],
                                  strategy_requirements: Dict[str, Any],
                                  market_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """智能筛选股票"""
        if not self.stock_screener:
            return {'error': 'AI股票筛选器未启用'}
        
        try:
            return self.stock_screener.process(stock_pool, strategy_requirements, market_data)
        except Exception as e:
            logger.error(f"股票筛选失败: {e}")
            return {'error': str(e)}
    
    def evaluate_strategy_confidence(self,
                                   strategy_name: str,
                                   market_data: Dict[str, pd.DataFrame],
                                   recent_signals: pd.DataFrame,
                                   market_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """评估策略置信度"""
        if not self.confidence_evaluator:
            return {'error': '置信度评估器未启用'}
        
        try:
            return self.confidence_evaluator.process(
                strategy_name, market_data, recent_signals, market_indicators
            )
        except Exception as e:
            logger.error(f"置信度评估失败: {e}")
            return {'error': str(e)}
    
    def get_ai_insights(self, 
                       trades_df: pd.DataFrame = None,
                       market_data: Dict[str, pd.DataFrame] = None,
                       strategy_name: str = None) -> Dict[str, Any]:
        """获取AI综合洞察"""
        
        insights = {
            'timestamp': pd.Timestamp.now(),
            'strategy_analysis': None,
            'market_insights': None,
            'recommendations': []
        }
        
        # 策略分析
        if trades_df is not None and not trades_df.empty:
            strategy_analysis = self.analyze_trading_history(trades_df)
            insights['strategy_analysis'] = strategy_analysis
            
            if 'recommendations' in strategy_analysis:
                insights['recommendations'].extend(strategy_analysis['recommendations'])
        
        # 市场洞察
        if market_data and strategy_name:
            # 构建市场指标
            market_indicators = self._calculate_market_indicators(market_data)
            
            # 评估置信度
            recent_signals = trades_df.tail(20) if trades_df is not None else pd.DataFrame()
            confidence_eval = self.evaluate_strategy_confidence(
                strategy_name, market_data, recent_signals, market_indicators
            )
            
            insights['market_insights'] = {
                'confidence_evaluation': confidence_eval,
                'market_indicators': market_indicators
            }
            
            # 添加建议
            if confidence_eval.get('recommendation'):
                insights['recommendations'].append(f"策略建议: {confidence_eval['recommendation']}")
        
        return insights
    
    def _calculate_market_indicators(self, market_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """计算市场指标"""
        indicators = {}
        
        if not market_data:
            return indicators
        
        # 计算市场整体波动率
        all_returns = []
        for stock, data in market_data.items():
            if len(data) >= 20:
                returns = data['close'].pct_change().dropna()
                all_returns.extend(returns.tail(20).tolist())
        
        if all_returns:
            indicators['volatility'] = pd.Series(all_returns).std()
        
        # 计算趋势强度（上涨股票比例）
        rising_count = 0
        total_count = 0
        
        for stock, data in market_data.items():
            if len(data) >= 5:
                recent_change = (data['close'].iloc[-1] - data['close'].iloc[-5]) / data['close'].iloc[-5]
                if recent_change > 0:
                    rising_count += 1
                total_count += 1
        
        if total_count > 0:
            indicators['trend_strength'] = rising_count / total_count
        
        # 市场情绪（简化版）
        indicators['sentiment'] = indicators.get('trend_strength', 0.5)
        
        return indicators
    
    def batch_process_strategies(self, strategy_descriptions: List[str]) -> List[Dict[str, Any]]:
        """批量处理策略描述"""
        results = []
        
        for i, description in enumerate(strategy_descriptions):
            logger.info(f"处理策略 {i+1}/{len(strategy_descriptions)}")
            
            result = self.generate_strategy_from_description(description)
            result['original_description'] = description
            results.append(result)
        
        return results
    
    def update_model_config(self, new_config: Dict[str, Any]):
        """更新模型配置"""
        self.model_config.update(new_config)
        
        # 重新初始化模块
        self._initialize_modules()
        logger.info("AI模块配置已更新")
    
    def get_module_status(self) -> Dict[str, bool]:
        """获取各模块状态"""
        return {
            'strategy_analyzer': self.strategy_analyzer is not None,
            'nlp_generator': self.nlp_generator is not None,
            'stock_screener': self.stock_screener is not None,
            'confidence_evaluator': self.confidence_evaluator is not None
        }