"""
迭代1 - 应用测试
"""
import pytest
import json
from app import app

@pytest.fixture
def client():
    """测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """测试首页"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'量化交易分析系统' in response.data

def test_analysis_page(client):
    """测试分析页面"""
    response = client.get('/analysis')
    assert response.status_code == 200
    assert b'股票分析' in response.data

def test_analyze_stock_api(client):
    """测试股票分析API"""
    response = client.get('/api/analyze/000001')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'symbol' in data
    assert 'ohlc_data' in data
    assert 'indicators' in data
    assert 'summary' in data

def test_stock_info_api(client):
    """测试股票信息API"""
    response = client.get('/api/stock_info/000001')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'symbol' in data
    assert 'name' in data

def test_search_stocks_api(client):
    """测试股票搜索API"""
    response = client.get('/api/search_stocks?q=000001')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'results' in data

def test_invalid_stock_code(client):
    """测试无效股票代码"""
    response = client.get('/api/analyze/invalid')
    # 应该返回错误或模拟数据
    assert response.status_code in [200, 400]

def test_empty_search_query(client):
    """测试空搜索查询"""
    response = client.get('/api/search_stocks?q=')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['results'] == []