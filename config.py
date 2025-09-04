# 配置文件
import os

class Config:
    # 数据源配置
    TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN', '')  # 需要申请tushare token
    
    # 交易配置
    INITIAL_CAPITAL = 100000  # 初始资金
    MAX_POSITION_RATIO = 0.3  # 最大单只股票仓位比例
    STOP_LOSS_RATIO = 0.05    # 止损比例 5%
    TAKE_PROFIT_RATIO = 0.15  # 止盈比例 15%
    
    # 缠论参数
    MIN_K_COUNT = 5           # 最小K线数量识别笔
    FRACTAL_THRESHOLD = 0.01  # 分型阈值
    
    # MACD参数
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    # 均线参数
    MA_SHORT = 5
    MA_MEDIUM = 20
    MA_LONG = 60
    
    # 数据库配置
    DB_PATH = 'data/trading.db'
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/trading.log'
    
    # AI模块配置
    AI_MODEL_CONFIG = {
        'type': 'openai',  # openai, claude, qwen, local
        'api_key': os.getenv('OPENAI_API_KEY', ''),
        'base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com'),
        'model_name': 'gpt-3.5-turbo',
        'max_tokens': 2000,
        'temperature': 0.7
    }
    
    # AI功能开关
    ENABLE_AI_STRATEGY_ANALYSIS = True
    ENABLE_AI_STOCK_SCREENING = True
    ENABLE_AI_CONFIDENCE_EVALUATION = True
    ENABLE_NLP_STRATEGY_GENERATION = True