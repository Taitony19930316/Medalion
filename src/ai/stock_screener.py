"""
AI股票筛选器 - 智能筛选符合策略的股票池
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from .base_ai_module import BaseAIModule

class AIStockScreener(BaseAIModule):
    """AI驱动的股票筛选器"""
    
    def __init__(self, model_config: Dict[str, Any]):
        super().__init__(model_config)
        
    def screen_stocks(self, 
                     stock_pool: List[str], 
                     strategy_requirements: Dict[str, Any],
                     market_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """智能筛选股票"""
        
        # 基础技术面筛选
        technical_filtered = self._technical_screening(stock_pool, market_data)
        
        # 基本面筛选（如果有数据）
        fundamental_filtered = self._fundamental_screening(technical_filtered, market_data)
        
        # AI深度分析
        ai_analysis = self._ai_deep_analysis(fundamental_filtered, strategy_requirements, market_data)
        
        return {
            'filtered_stocks': ai_analysis['recommended_stocks'],
            'analysis_report': ai_analysis['analysis'],
            'confidence_scores': ai_analysis['confidence_scores'],
            'risk_warnings': ai_analysis['risk_warnings']
        }
    
    def _technical_screening(self, stock_pool: List[str], market_data: Dict[str, pd.DataFrame]) -> List[str]:
        """技术面初步筛选"""
        filtered_stocks = []
        
        for stock in stock_pool:
            if stock not in market_data:
                continue
                
            data = market_data[stock]
            if len(data) < 60:  # 至少需要60天数据
                continue
                
            # 基础技术条件筛选
            latest = data.iloc[-1]
            
            # 1. 价格在合理范围内（避免ST股等）
            if latest['close'] < 2 or latest['close'] > 300:
                continue
                
            # 2. 成交量活跃
            avg_volume = data['volume'].tail(20).mean()
            if avg_volume < 1000000:  # 日均成交量至少100万
                continue
                
            # 3. 价格波动合理
            volatility = data['close'].pct_change().tail(20).std()
            if volatility > 0.1:  # 日波动率不超过10%
                continue
                
            filtered_stocks.append(stock)
            
        return filtered_stocks
    
    def _fundamental_screening(self, stock_pool: List[str], market_data: Dict[str, pd.DataFrame]) -> List[str]:
        """基本面筛选（简化版）"""
        # 这里可以接入基本面数据进行筛选
        # 暂时返回技术面筛选结果
        return stock_pool
    
    def _ai_deep_analysis(self, 
                         stock_pool: List[str], 
                         strategy_requirements: Dict[str, Any],
                         market_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """AI深度分析筛选"""
        
        # 为每只股票生成分析报告
        stock_analyses = {}
        confidence_scores = {}
        
        for stock in stock_pool[:20]:  # 限制分析数量，避免API调用过多
            analysis = self._analyze_single_stock(stock, strategy_requirements, market_data.get(stock))
            stock_analyses[stock] = analysis
            confidence_scores[stock] = analysis.get('confidence_score', 0)
        
        # 根据置信度排序
        sorted_stocks = sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 生成综合分析报告
        comprehensive_analysis = self._generate_comprehensive_analysis(
            sorted_stocks, stock_analyses, strategy_requirements
        )
        
        return {
            'recommended_stocks': [stock for stock, score in sorted_stocks if score > 0.6],
            'analysis': comprehensive_analysis,
            'confidence_scores': confidence_scores,
            'risk_warnings': self._generate_risk_warnings(sorted_stocks, stock_analyses)
        }
    
    def _analyze_single_stock(self, 
                            stock: str, 
                            strategy_requirements: Dict[str, Any],
                            stock_data: pd.DataFrame) -> Dict[str, Any]:
        """分析单只股票"""
        
        if stock_data is None or len(stock_data) < 30:
            return {'confidence_score': 0, 'reason': '数据不足'}
        
        # 生成股票分析提示词
        prompt = self._build_stock_analysis_prompt(stock, strategy_requirements, stock_data)
        
        system_prompt = """你是专业的股票分析师，请根据提供的数据和策略要求分析股票。
        
        请按以下JSON格式输出分析结果：
        {
            "confidence_score": 0.85,  // 0-1之间的置信度分数
            "technical_analysis": "技术面分析",
            "strategy_fit": "与策略的匹配度分析", 
            "risk_factors": ["风险因素1", "风险因素2"],
            "opportunity_factors": ["机会因素1", "机会因素2"],
            "recommendation": "买入/观望/回避",
            "target_price": "目标价位",
            "stop_loss": "建议止损位"
        }"""
        
        try:
            analysis_result = self.call_llm(prompt, system_prompt)
            # 这里应该解析JSON，简化处理
            return {
                'confidence_score': np.random.uniform(0.3, 0.9),  # 临时随机值
                'analysis': analysis_result
            }
        except Exception as e:
            return {'confidence_score': 0, 'error': str(e)}
    
    def _build_stock_analysis_prompt(self, 
                                   stock: str, 
                                   strategy_requirements: Dict[str, Any],
                                   stock_data: pd.DataFrame) -> str:
        """构建股票分析提示词"""
        
        # 计算关键技术指标
        latest_data = stock_data.tail(10)
        
        prompt = f"""
        请分析股票 {stock}：
        
        ## 策略要求
        {strategy_requirements}
        
        ## 最近10天数据
        {latest_data.to_string()}
        
        ## 技术指标概况
        - 当前价格: {stock_data['close'].iloc[-1]:.2f}
        - 20日均价: {stock_data['close'].tail(20).mean():.2f}
        - 成交量变化: {stock_data['volume'].tail(5).mean() / stock_data['volume'].tail(20).mean():.2f}
        - 价格波动率: {stock_data['close'].pct_change().tail(20).std():.4f}
        
        请根据策略要求分析该股票的投资价值和风险。
        """
        
        return prompt
    
    def _generate_comprehensive_analysis(self, 
                                       sorted_stocks: List[tuple], 
                                       stock_analyses: Dict[str, Any],
                                       strategy_requirements: Dict[str, Any]) -> str:
        """生成综合分析报告"""
        
        top_stocks = sorted_stocks[:10]
        
        prompt = f"""
        基于以下股票筛选结果，生成综合分析报告：
        
        ## 策略要求
        {strategy_requirements}
        
        ## 推荐股票（按置信度排序）
        {[(stock, f"{score:.2f}") for stock, score in top_stocks]}
        
        ## 个股分析摘要
        {[f"{stock}: {analysis.get('analysis', '')[:200]}..." for stock, analysis in list(stock_analyses.items())[:5]]}
        
        请生成一份简洁的市场分析报告，包括：
        1. 当前市场环境评估
        2. 推荐股票的共同特征
        3. 投资建议和注意事项
        4. 风险提示
        """
        
        system_prompt = "你是资深投资顾问，请生成专业的股票筛选分析报告。"
        
        return self.call_llm(prompt, system_prompt)
    
    def _generate_risk_warnings(self, 
                              sorted_stocks: List[tuple], 
                              stock_analyses: Dict[str, Any]) -> List[str]:
        """生成风险警告"""
        warnings = []
        
        # 检查整体置信度分布
        scores = [score for _, score in sorted_stocks]
        if len(scores) > 0:
            avg_score = np.mean(scores)
            if avg_score < 0.5:
                warnings.append("整体股票池质量偏低，建议谨慎投资")
            
            if len([s for s in scores if s > 0.8]) == 0:
                warnings.append("缺乏高置信度标的，建议等待更好机会")
        
        return warnings
    
    def process(self, 
               stock_pool: List[str], 
               strategy_requirements: Dict[str, Any],
               market_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """主要处理方法"""
        return self.screen_stocks(stock_pool, strategy_requirements, market_data)