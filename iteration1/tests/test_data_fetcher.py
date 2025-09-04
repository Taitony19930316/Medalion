"""
数据获取模块测试
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta
from data.fetcher import DataFetcher

@pytest.fixture
def data_fetcher():
    """数据获取器实例"""
    return DataFetcher()

def test_data_fetcher_init(data_fetcher):
    """测试数据获取器初始化"""
    assert data_fetcher is not None
    assert hasattr(data_fetcher, 'cache_db')

def test_get_stock_data(data_fetcher):
    """测试获取股票数据"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    data = data_fetcher.get_stock_data(
        symbol='000001',
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )
    
    assert data is not None
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
    assert all(col in data.columns for col in ['open', 'high', 'low', 'close', 'volume'])

def test_get_stock_info(data_fetcher):
    """测试获取股票信息"""
    info = data_fetcher.get_stock_info('000001')
    
    assert info is not None
    assert isinstance(info, dict)
    assert 'symbol' in info
    assert 'name' in info

def test_search_stocks(data_fetcher):
    """测试搜索股票"""
    results = data_fetcher.search_stocks('000001')
    
    assert isinstance(results, list)
    if results:
        assert 'symbol' in results[0]
        assert 'name' in results[0]

def test_generate_mock_data(data_fetcher):
    """测试生成模拟数据"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    data = data_fetcher._generate_mock_data(
        symbol='TEST001',
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d')
    )
    
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
    assert all(col in data.columns for col in ['open', 'high', 'low', 'close', 'volume'])
    
    # 验证数据合理性
    assert (data['high'] >= data['low']).all()
    assert (data['high'] >= data['open']).all()
    assert (data['high'] >= data['close']).all()
    assert (data['low'] <= data['open']).all()
    assert (data['low'] <= data['close']).all()
    assert (data['volume'] > 0).all()