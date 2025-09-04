"""
自然语言策略生成器 - 根据文字描述生成可执行的交易策略
"""
import json
import re
from typing import Dict, List, Any, Optional
from .base_ai_module import BaseAIModule

class NLPStrategyGenerator(BaseAIModule):
    """自然语言策略生成器"""
    
    def __init__(self, model_config: Dict[str, Any]):
        super().__init__(model_config)
        
    def generate_strategy_from_text(self, description: str) -> Dict[str, Any]:
        """根据文字描述生成策略"""
        
        # 构建策略生成提示词
        prompt = self._build_strategy_prompt(description)
        
        system_prompt = """你是一个专业的量化交易策略开发专家。
        用户会用自然语言描述一个交易想法，你需要将其转换为结构化的交易策略。
        
        请按照以下JSON格式输出策略：
        {
            "strategy_name": "策略名称",
            "description": "策略描述", 
            "entry_conditions": ["入场条件1", "入场条件2"],
            "exit_conditions": ["出场条件1", "出场条件2"],
            "risk_management": {
                "stop_loss": "止损条件",
                "take_profit": "止盈条件",
                "position_size": "仓位管理"
            },
            "indicators": ["需要的技术指标"],
            "timeframe": "时间周期",
            "market_conditions": "适用市场环境",
            "code_template": "Python代码模板"
        }
        
        确保策略逻辑清晰、可执行，并包含完整的风险管理措施。"""
        
        # 调用大模型生成策略
        strategy_json = self.call_llm(prompt, system_prompt)
        
        try:
            # 解析JSON结果
            strategy_dict = json.loads(self._extract_json(strategy_json))
            
            # 生成可执行代码
            executable_code = self._generate_executable_code(strategy_dict)
            strategy_dict['executable_code'] = executable_code
            
            return strategy_dict
            
        except Exception as e:
            return {
                'error': f'策略生成失败: {str(e)}',
                'raw_response': strategy_json
            }
    
    def _build_strategy_prompt(self, description: str) -> str:
        """构建策略生成提示词"""
        
        prompt = f"""
        用户策略描述：
        {description}
        
        请将上述描述转换为完整的量化交易策略。
        
        注意事项：
        1. 策略必须包含明确的入场和出场条件
        2. 必须有完整的风险管理措施
        3. 技术指标的参数要具体
        4. 考虑不同市场环境的适应性
        5. 代码模板要能直接运行
        
        如果描述中提到了缠论、MACD、均线等技术分析方法，请详细展开相关的判断逻辑。
        """
        
        return prompt
    
    def _extract_json(self, text: str) -> str:
        """从文本中提取JSON部分"""
        # 查找JSON代码块
        json_pattern = r'```json\s*(.*?)\s*```'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            return match.group(1)
        
        # 查找大括号包围的JSON
        brace_pattern = r'\{.*\}'
        match = re.search(brace_pattern, text, re.DOTALL)
        if match:
            return match.group(0)
            
        return text
    
    def _generate_executable_code(self, strategy_dict: Dict[str, Any]) -> str:
        """生成可执行的策略代码"""
        
        code_template = f'''
"""
{strategy_dict.get('strategy_name', '未命名策略')}
{strategy_dict.get('description', '')}
"""

import pandas as pd
import numpy as np
from src.strategies.base_strategy import BaseStrategy

class GeneratedStrategy(BaseStrategy):
    def __init__(self, params=None):
        super().__init__(params or {{}})
        self.name = "{strategy_dict.get('strategy_name', 'Generated Strategy')}"
        
        # 策略参数
        self.timeframe = "{strategy_dict.get('timeframe', '1d')}"
        self.indicators = {strategy_dict.get('indicators', [])}
        
    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算交易信号"""
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0
        
        # 入场条件
        entry_conditions = {strategy_dict.get('entry_conditions', [])}
        
        # 出场条件  
        exit_conditions = {strategy_dict.get('exit_conditions', [])}
        
        # TODO: 根据具体条件实现信号逻辑
        # 这里需要根据strategy_dict中的条件生成具体的计算逻辑
        
        return signals
        
    def get_risk_management(self) -> dict:
        """获取风险管理参数"""
        return {strategy_dict.get('risk_management', {{}})}
        
    def is_market_suitable(self, market_data: pd.DataFrame) -> bool:
        """判断市场环境是否适合该策略"""
        # 根据market_conditions判断
        return True
'''
        
        return code_template
    
    def optimize_strategy_description(self, description: str) -> str:
        """优化策略描述，使其更适合生成代码"""
        
        prompt = f"""
        请优化以下策略描述，使其更加具体和可执行：
        
        原始描述：
        {description}
        
        请从以下角度进行优化：
        1. 明确技术指标的具体参数
        2. 详细描述入场和出场条件
        3. 补充风险管理措施
        4. 指定适用的时间周期
        5. 说明适用的市场环境
        
        输出优化后的策略描述。
        """
        
        system_prompt = "你是量化交易专家，擅长将模糊的交易想法转换为精确的策略描述。"
        
        return self.call_llm(prompt, system_prompt)
    
    def process(self, description: str, optimize: bool = True) -> Dict[str, Any]:
        """主要处理方法"""
        if optimize:
            description = self.optimize_strategy_description(description)
            
        return self.generate_strategy_from_text(description)