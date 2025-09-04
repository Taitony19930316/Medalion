"""
策略分析器 - 自动提炼和总结交易策略
"""
import pandas as pd
from typing import Dict, List, Any
from .base_ai_module import BaseAIModule

class StrategyAnalyzer(BaseAIModule):
    """策略分析器 - 分析历史交易记录，提炼成功模式"""
    
    def __init__(self, model_config: Dict[str, Any]):
        super().__init__(model_config)
        
    def analyze_trading_history(self, trades_df: pd.DataFrame) -> Dict[str, Any]:
        """分析交易历史，提炼策略模式"""
        
        # 计算基础统计信息
        stats = self._calculate_trade_stats(trades_df)
        
        # 生成分析提示词
        prompt = self._generate_analysis_prompt(trades_df, stats)
        
        system_prompt = """你是一个专业的量化交易策略分析师。
        请分析提供的交易数据，识别出成功的交易模式和策略特征。
        重点关注：
        1. 盈利交易的共同特征
        2. 亏损交易的风险模式
        3. 最佳入场和出场时机
        4. 技术指标的有效组合
        5. 市场环境的影响因素
        
        请用结构化的方式输出分析结果。"""
        
        # 调用大模型分析
        analysis_result = self.call_llm(prompt, system_prompt)
        
        return {
            'basic_stats': stats,
            'ai_analysis': analysis_result,
            'recommendations': self._extract_recommendations(analysis_result)
        }
    
    def _calculate_trade_stats(self, trades_df: pd.DataFrame) -> Dict[str, Any]:
        """计算交易统计信息"""
        if trades_df.empty:
            return {}
            
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['profit'] > 0])
        losing_trades = len(trades_df[trades_df['profit'] < 0])
        
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        avg_profit = trades_df['profit'].mean()
        max_profit = trades_df['profit'].max()
        max_loss = trades_df['profit'].min()
        
        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'profit_factor': abs(trades_df[trades_df['profit'] > 0]['profit'].sum() / 
                               trades_df[trades_df['profit'] < 0]['profit'].sum()) if losing_trades > 0 else float('inf')
        }
    
    def _generate_analysis_prompt(self, trades_df: pd.DataFrame, stats: Dict) -> str:
        """生成分析提示词"""
        
        # 获取盈利和亏损交易的样本
        profitable_trades = trades_df[trades_df['profit'] > 0].head(10)
        losing_trades = trades_df[trades_df['profit'] < 0].head(10)
        
        prompt = f"""
        请分析以下交易数据：
        
        ## 基础统计
        - 总交易次数: {stats.get('total_trades', 0)}
        - 胜率: {stats.get('win_rate', 0):.2%}
        - 平均收益: {stats.get('avg_profit', 0):.2f}
        - 最大盈利: {stats.get('max_profit', 0):.2f}
        - 最大亏损: {stats.get('max_loss', 0):.2f}
        - 盈亏比: {stats.get('profit_factor', 0):.2f}
        
        ## 盈利交易样本
        {profitable_trades.to_string() if not profitable_trades.empty else '无盈利交易'}
        
        ## 亏损交易样本  
        {losing_trades.to_string() if not losing_trades.empty else '无亏损交易'}
        
        请深入分析这些数据，找出成功交易的关键因素和失败交易的风险点。
        """
        
        return prompt
    
    def _extract_recommendations(self, analysis_result: str) -> List[str]:
        """从分析结果中提取建议"""
        # 这里可以用更复杂的NLP方法提取关键建议
        # 简单实现：按行分割，提取包含"建议"、"应该"等关键词的句子
        lines = analysis_result.split('\n')
        recommendations = []
        
        keywords = ['建议', '应该', '需要', '可以', '推荐']
        for line in lines:
            if any(keyword in line for keyword in keywords):
                recommendations.append(line.strip())
                
        return recommendations[:10]  # 最多返回10条建议
    
    def process(self, trades_df: pd.DataFrame) -> Dict[str, Any]:
        """主要处理方法"""
        return self.analyze_trading_history(trades_df)