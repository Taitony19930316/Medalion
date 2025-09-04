"""
迭代1配置文件
"""
import os

class Config:
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 5000)
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # 数据源配置
    TUSHARE_TOKEN = os.environ.get('TUSHARE_TOKEN') or ''
    AKSHARE_ENABLED = os.environ.get('AKSHARE_ENABLED', 'True').lower() == 'true'
    
    # 数据库配置
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///data/stocks.db'
    
    # 缓存配置
    CACHE_ENABLED = True
    CACHE_TIMEOUT = 300  # 5分钟缓存
    
    # API限制
    MAX_REQUESTS_PER_MINUTE = 60
    
    # 技术指标参数
    MA_PERIODS = [5, 20, 60]
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    RSI_PERIOD = 14
    
    # 缠论参数
    MIN_FRACTAL_STRENGTH = 3  # 分型最小强度
    FRACTAL_LOOKBACK = 2      # 分型识别回看周期
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/app.log'
    
    # 前端配置
    CHART_DEFAULT_PERIOD = 60  # 默认显示60天数据
    CHART_MAX_POINTS = 500     # 图表最大数据点数

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

# 根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

Config = config[os.environ.get('FLASK_ENV', 'default')]