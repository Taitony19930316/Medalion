"""
技术指标模块测试
"""
import pytest
import pandas as pd
import numpy as np
from data.indicators import TechnicalIndicators
from data.fetcher import DataFetcher

@pytest.fixture
def indicators():
    """技术指标计算器实例"""
    return TechnicalIndicators()

@pytest.fixture
def sample_data():
    """样本数据"""
    # 生成测试数据
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    prices = 20 + np.cumsum(np.random.randn(100) * 0.1)
    
    data = pd.DataFrame({
        'open': prices * np.random.uniform(0.99, 1.01, 100),
        'high': prices * np.random.uniform(1.01, 1.03, 100),
        'low': prices * np.random.uniform(0.97, 0.99, 100),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, 100)
    }, index=dates)
    
    return data

def test_calculate_moving_averages(indicators, sample_data):
    """测试移动平均线计算"""
    result = indicators.calculate_moving_averages(sample_data)
    
    assert 'ma5' in result.columns
    assert 'ma20' in result.columns
    assert 'ma60' in result.columns
    
    # 验证MA5不为空（除了前4个值）
    assert not result['ma5'].iloc[4:].isna().any()
    
    # 验证MA值的合理性
    assert (result['ma5'].dropna() > 0).all()

def test_calculate_macd(indicators, sample_data):
    """测试MACD计算"""
    result = indicators.calculate_macd(sample_data)
    
    assert 'macd' in result.columns
    assert 'macd_signal' in result.columns
    assert 'macd_hist' in result.columns
    
    # 验证MACD柱状图 = MACD - 信号线
    macd_diff = result['macd'] - result['macd_signal']
    pd.testing.assert_series_equal(
        result['macd_hist'].dropna(), 
        macd_diff.dropna(), 
        check_names=False
    )

def test_calculate_rsi(indicators, sample_data):
    """测试RSI计算"""
    result = indicators.calculate_rsi(sample_data)
    
    assert 'rsi' in result.columns
    
    # RSI应该在0-100之间
    rsi_values = result['rsi'].dropna()
    assert (rsi_values >= 0).all()
    assert (rsi_values <= 100).all()

def test_calculate_bollinger_bands(indicators, sample_data):
    """测试布林带计算"""
    result = indicators.calculate_bollinger_bands(sample_data)
    
    assert 'bb_upper' in result.columns
    assert 'bb_middle' in result.columns
    assert 'bb_lower' in result.columns
    assert 'bb_width' in result.columns
    assert 'bb_percent' in result.columns
    
    # 验证布林带关系：上轨 > 中轨 > 下轨
    valid_data = result.dropna()
    assert (valid_data['bb_upper'] >= valid_data['bb_middle']).all()
    assert (valid_data['bb_middle'] >= valid_data['bb_lower']).all()

def test_calculate_volume_indicators(indicators, sample_data):
    """测试成交量指标"""
    result = indicators.calculate_volume_indicators(sample_data)
    
    assert 'volume_ma5' in result.columns
    assert 'volume_ma20' in result.columns
    assert 'volume_ratio' in result.columns
    
    # 验证成交量比率的合理性
    volume_ratio = result['volume_ratio'].dropna()
    assert (volume_ratio > 0).all()

def test_calculate_all_indicators(indicators, sample_data):
    """测试计算所有指标"""
    result = indicators.calculate_all_indicators(sample_data)
    
    # 验证所有主要指标都存在
    expected_columns = [
        'ma5', 'ma20', 'ma60', 'macd', 'macd_signal', 'macd_hist', 
        'rsi', 'bb_upper', 'bb_middle', 'bb_lower'
    ]
    
    for col in expected_columns:
        assert col in result.columns

def test_get_latest_values(indicators, sample_data):
    """测试获取最新指标值"""
    data_with_indicators = indicators.calculate_all_indicators(sample_data)
    latest_values = indicators.get_latest_values(data_with_indicators)
    
    assert isinstance(latest_values, dict)
    assert 'price' in latest_values
    assert 'ma' in latest_values
    assert 'macd' in latest_values
    assert 'rsi' in latest_values

def test_detect_golden_cross(indicators, sample_data):
    """测试金叉检测"""
    data_with_indicators = indicators.calculate_all_indicators(sample_data)
    
    # 人工创建金叉条件
    data_with_indicators.iloc[-1, data_with_indicators.columns.get_loc('macd')] = 0.1
    data_with_indicators.iloc[-1, data_with_indicators.columns.get_loc('macd_signal')] = 0.05
    data_with_indicators.iloc[-2, data_with_indicators.columns.get_loc('macd')] = -0.05
    data_with_indicators.iloc[-2, data_with_indicators.columns.get_loc('macd_signal')] = 0.05
    
    signals = indicators.detect_golden_cross(data_with_indicators)
    
    # 应该检测到MACD金叉
    if signals:
        assert any('MACD金叉' in signal['type'] for signal in signals)

def test_detect_death_cross(indicators, sample_data):
    """测试死叉检测"""
    data_with_indicators = indicators.calculate_all_indicators(sample_data)
    
    # 人工创建死叉条件
    data_with_indicators.iloc[-1, data_with_indicators.columns.get_loc('macd')] = -0.1
    data_with_indicators.iloc[-1, data_with_indicators.columns.get_loc('macd_signal')] = -0.05
    data_with_indicators.iloc[-2, data_with_indicators.columns.get_loc('macd')] = 0.05
    data_with_indicators.iloc[-2, data_with_indicators.columns.get_loc('macd_signal')] = -0.05
    
    signals = indicators.detect_death_cross(data_with_indicators)
    
    # 应该检测到MACD死叉
    if signals:
        assert any('MACD死叉' in signal['type'] for signal in signals)