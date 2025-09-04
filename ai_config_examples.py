"""
AI模型配置示例
支持多种大模型接入方式
"""
import os

# ================================
# OpenAI GPT 配置示例
# ================================
OPENAI_CONFIG = {
    'type': 'openai',
    'api_key': os.getenv('OPENAI_API_KEY'),
    'base_url': 'https://api.openai.com',  # 或使用代理地址
    'model_name': 'gpt-3.5-turbo',  # 或 'gpt-4'
    'temperature': 0.7,
    'max_tokens': 2000
}

# ================================
# Anthropic Claude 配置示例
# ================================
CLAUDE_CONFIG = {
    'type': 'claude',
    'api_key': os.getenv('ANTHROPIC_API_KEY'),
    'base_url': 'https://api.anthropic.com',
    'model_name': 'claude-3-sonnet-20240229',
    'temperature': 0.7,
    'max_tokens': 2000
}

# ================================
# 阿里云通义千问配置示例
# ================================
QWEN_CONFIG = {
    'type': 'qwen',
    'api_key': os.getenv('DASHSCOPE_API_KEY'),
    'base_url': 'https://dashscope.aliyuncs.com',
    'model_name': 'qwen-turbo',  # 或 'qwen-plus', 'qwen-max'
    'temperature': 0.7,
    'max_tokens': 2000
}

# ================================
# 本地模型 (Ollama) 配置示例
# ================================
LOCAL_CONFIG = {
    'type': 'local',
    'base_url': 'http://localhost:11434',  # Ollama默认地址
    'model_name': 'llama2',  # 或其他本地模型
    'temperature': 0.7,
    'max_tokens': 2000
}

# ================================
# 百度文心一言配置示例
# ================================
ERNIE_CONFIG = {
    'type': 'ernie',
    'api_key': os.getenv('BAIDU_API_KEY'),
    'secret_key': os.getenv('BAIDU_SECRET_KEY'),
    'base_url': 'https://aip.baidubce.com',
    'model_name': 'ernie-bot-turbo',
    'temperature': 0.7,
    'max_tokens': 2000
}

# ================================
# 使用示例
# ================================
def get_ai_config(model_type='openai'):
    """获取指定类型的AI配置"""
    configs = {
        'openai': OPENAI_CONFIG,
        'claude': CLAUDE_CONFIG,
        'qwen': QWEN_CONFIG,
        'local': LOCAL_CONFIG,
        'ernie': ERNIE_CONFIG
    }
    
    return configs.get(model_type, OPENAI_CONFIG)

# ================================
# 环境变量设置指南
# ================================
ENV_SETUP_GUIDE = """
# 设置环境变量 (Linux/Mac)
export OPENAI_API_KEY="sk-your-openai-key"
export ANTHROPIC_API_KEY="your-claude-key"
export DASHSCOPE_API_KEY="your-qwen-key"
export BAIDU_API_KEY="your-baidu-key"
export BAIDU_SECRET_KEY="your-baidu-secret"

# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-openai-key"
$env:ANTHROPIC_API_KEY="your-claude-key"

# 或者在代码中直接设置 (不推荐用于生产环境)
os.environ['OPENAI_API_KEY'] = 'your-key-here'
"""

# ================================
# API密钥获取指南
# ================================
API_KEY_GUIDE = {
    'openai': {
        'url': 'https://platform.openai.com/api-keys',
        'description': 'OpenAI官方API密钥，需要信用卡验证',
        'cost': '按使用量计费，GPT-3.5约$0.002/1K tokens'
    },
    'claude': {
        'url': 'https://console.anthropic.com/',
        'description': 'Anthropic Claude API密钥',
        'cost': '按使用量计费，价格与GPT相近'
    },
    'qwen': {
        'url': 'https://dashscope.console.aliyun.com/',
        'description': '阿里云通义千问，国内访问稳定',
        'cost': '相对便宜，支持人民币付费'
    },
    'local': {
        'url': 'https://ollama.ai/',
        'description': '本地部署，完全免费但需要较好硬件',
        'cost': '免费，但需要本地GPU资源'
    }
}

def print_setup_guide():
    """打印设置指南"""
    print("🔧 AI模型配置指南")
    print("=" * 50)
    
    print("\n📋 支持的模型:")
    for model_type, info in API_KEY_GUIDE.items():
        print(f"\n{model_type.upper()}:")
        print(f"  获取地址: {info['url']}")
        print(f"  说明: {info['description']}")
        print(f"  成本: {info['cost']}")
    
    print(f"\n💡 环境变量设置:")
    print(ENV_SETUP_GUIDE)
    
    print("\n🚀 快速开始:")
    print("1. 选择一个模型提供商")
    print("2. 获取API密钥")
    print("3. 设置环境变量")
    print("4. 在config.py中选择对应配置")
    print("5. 运行 python start_here.py 开始使用")

if __name__ == "__main__":
    print_setup_guide()