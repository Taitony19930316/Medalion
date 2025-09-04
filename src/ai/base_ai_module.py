"""
AI模块基类
支持多种大模型接入：OpenAI、Claude、国产大模型等
"""
import json
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from loguru import logger

class BaseAIModule(ABC):
    """AI模块基类"""
    
    def __init__(self, model_config: Dict[str, Any]):
        self.model_config = model_config
        self.model_type = model_config.get('type', 'openai')
        self.api_key = model_config.get('api_key')
        self.base_url = model_config.get('base_url')
        self.model_name = model_config.get('model_name', 'gpt-3.5-turbo')
        
    def call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """调用大模型API"""
        try:
            if self.model_type == 'openai':
                return self._call_openai(prompt, system_prompt)
            elif self.model_type == 'claude':
                return self._call_claude(prompt, system_prompt)
            elif self.model_type == 'qwen':
                return self._call_qwen(prompt, system_prompt)
            elif self.model_type == 'local':
                return self._call_local_model(prompt, system_prompt)
            else:
                raise ValueError(f"不支持的模型类型: {self.model_type}")
        except Exception as e:
            logger.error(f"调用大模型失败: {e}")
            return ""
    
    def _call_openai(self, prompt: str, system_prompt: str = None) -> str:
        """调用OpenAI API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        url = f"{self.base_url or 'https://api.openai.com'}/v1/chat/completions"
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            raise Exception(f"API调用失败: {response.status_code}")
    
    def _call_claude(self, prompt: str, system_prompt: str = None) -> str:
        """调用Claude API"""
        # 实现Claude API调用逻辑
        pass
    
    def _call_qwen(self, prompt: str, system_prompt: str = None) -> str:
        """调用通义千问API"""
        # 实现通义千问API调用逻辑
        pass
    
    def _call_local_model(self, prompt: str, system_prompt: str = None) -> str:
        """调用本地模型（如ollama）"""
        # 实现本地模型调用逻辑
        pass
    
    @abstractmethod
    def process(self, *args, **kwargs) -> Any:
        """子类需要实现的核心处理方法"""
        pass