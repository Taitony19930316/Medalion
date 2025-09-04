"""
迭代1: 基础数据分析MVP - Flask主应用
提供股票数据获取、技术指标计算和基础缠论分析的Web界面
"""
from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, timedelta
import logging

from data.fetcher import DataFetcher
from data.indicators import TechnicalIndicators
from data.changlun import BasicChangLun
from config import Config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# 初始化组件
data_fetcher = DataFetcher()
tech_indicators = TechnicalIndicators()
changlun_analyzer = BasicChangLun()

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    """分析页面"""
    return render_template('analysis.html')

@app.route('/api/analyze/<symbol>')
def analyze_stock(symbol):
    """
    分析指定股票
    返回K线数据、技术指标和缠论分析结果
    """
    try:
        logger.info(f"开始分析股票: {symbol}")
        
        # 1. 获取股票数据
        end_date = datetime.now()
        start_date = end_date - timedelta(days=120)  # 获取120天数据
        
        stock_data = data_fetcher.get_stock_data(
            symbol=symbol,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        if stock_data is None or len(stock_data) == 0:
            return jsonify({'error': f'无法获取股票 {symbol} 的数据'}), 400
        
        logger.info(f"获取到 {len(stock_data)} 条数据")
        
        # 2. 计算技术指标
        stock_data_with_indicators = tech_indicators.calculate_all_indicators(stock_data)
        
        # 3. 缠论分析
        changlun_result = changlun_analyzer.analyze(stock_data_with_indicators)
        
        # 4. 准备返回数据
        result = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'data_points': len(stock_data_with_indicators),
            'ohlc_data': prepare_ohlc_data(stock_data_with_indicators),
            'indicators': prepare_indicators_data(stock_data_with_indicators),
            'changlun_analysis': changlun_result,
            'summary': generate_analysis_summary(stock_data_with_indicators, changlun_result)
        }
        
        logger.info(f"分析完成: {symbol}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"分析股票 {symbol} 时出错: {str(e)}")
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

@app.route('/api/stock_info/<symbol>')
def get_stock_info(symbol):
    """获取股票基本信息"""
    try:
        stock_info = data_fetcher.get_stock_info(symbol)
        return jsonify(stock_info)
    except Exception as e:
        logger.error(f"获取股票信息失败: {str(e)}")
        return jsonify({'error': '获取股票信息失败'}), 500

@app.route('/api/search_stocks')
def search_stocks():
    """搜索股票"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify({'results': []})
    
    try:
        results = data_fetcher.search_stocks(query)
        return jsonify({'results': results})
    except Exception as e:
        logger.error(f"搜索股票失败: {str(e)}")
        return jsonify({'error': '搜索失败'}), 500

def prepare_ohlc_data(df):
    """准备OHLC数据用于图表显示"""
    ohlc_data = []
    
    for index, row in df.iterrows():
        ohlc_data.append({
            'date': index.strftime('%Y-%m-%d'),
            'open': round(float(row['open']), 2),
            'high': round(float(row['high']), 2),
            'low': round(float(row['low']), 2),
            'close': round(float(row['close']), 2),
            'volume': int(row['volume'])
        })
    
    return ohlc_data

def prepare_indicators_data(df):
    """准备技术指标数据"""
    indicators = {}
    
    # 移动平均线
    if 'ma5' in df.columns:
        indicators['ma5'] = [{'date': idx.strftime('%Y-%m-%d'), 'value': round(float(val), 2)} 
                            for idx, val in df['ma5'].dropna().items()]
    
    if 'ma20' in df.columns:
        indicators['ma20'] = [{'date': idx.strftime('%Y-%m-%d'), 'value': round(float(val), 2)} 
                             for idx, val in df['ma20'].dropna().items()]
    
    if 'ma60' in df.columns:
        indicators['ma60'] = [{'date': idx.strftime('%Y-%m-%d'), 'value': round(float(val), 2)} 
                             for idx, val in df['ma60'].dropna().items()]
    
    # MACD
    if all(col in df.columns for col in ['macd', 'macd_signal', 'macd_hist']):
        indicators['macd'] = {
            'macd': [{'date': idx.strftime('%Y-%m-%d'), 'value': round(float(val), 4)} 
                    for idx, val in df['macd'].dropna().items()],
            'signal': [{'date': idx.strftime('%Y-%m-%d'), 'value': round(float(val), 4)} 
                      for idx, val in df['macd_signal'].dropna().items()],
            'histogram': [{'date': idx.strftime('%Y-%m-%d'), 'value': round(float(val), 4)} 
                         for idx, val in df['macd_hist'].dropna().items()]
        }
    
    # RSI
    if 'rsi' in df.columns:
        indicators['rsi'] = [{'date': idx.strftime('%Y-%m-%d'), 'value': round(float(val), 2)} 
                            for idx, val in df['rsi'].dropna().items()]
    
    return indicators

def generate_analysis_summary(df, changlun_result):
    """生成分析摘要"""
    latest = df.iloc[-1]
    
    # 基础信息
    summary = {
        'current_price': round(float(latest['close']), 2),
        'price_change': round(float(latest['close'] - df.iloc[-2]['close']), 2),
        'price_change_pct': round(float((latest['close'] - df.iloc[-2]['close']) / df.iloc[-2]['close'] * 100), 2),
        'volume': int(latest['volume']),
        'rsi': round(float(latest['rsi']), 2) if 'rsi' in df.columns else None
    }
    
    # 趋势判断
    if all(col in df.columns for col in ['ma5', 'ma20', 'ma60']):
        ma5 = latest['ma5']
        ma20 = latest['ma20']
        ma60 = latest['ma60']
        
        if ma5 > ma20 > ma60:
            summary['trend'] = '多头排列'
            summary['trend_strength'] = 'strong_up'
        elif ma5 < ma20 < ma60:
            summary['trend'] = '空头排列'
            summary['trend_strength'] = 'strong_down'
        else:
            summary['trend'] = '震荡整理'
            summary['trend_strength'] = 'sideways'
    
    # 缠论分析摘要
    if changlun_result:
        summary['changlun'] = {
            'fractals_count': len(changlun_result.get('fractals', [])),
            'recent_fractal': changlun_result.get('recent_fractal'),
            'trend_direction': changlun_result.get('trend_direction', 'unknown')
        }
    
    # 交易建议
    summary['suggestion'] = generate_trading_suggestion(summary, changlun_result)
    
    return summary

def generate_trading_suggestion(summary, changlun_result):
    """生成交易建议"""
    suggestions = []
    
    # 基于趋势的建议
    if summary.get('trend_strength') == 'strong_up':
        suggestions.append('多头趋势明确，可关注回调买点')
    elif summary.get('trend_strength') == 'strong_down':
        suggestions.append('空头趋势明确，建议谨慎操作')
    else:
        suggestions.append('震荡行情，建议区间操作')
    
    # 基于RSI的建议
    rsi = summary.get('rsi')
    if rsi:
        if rsi > 80:
            suggestions.append('RSI超买，注意回调风险')
        elif rsi < 20:
            suggestions.append('RSI超卖，可关注反弹机会')
    
    # 基于缠论的建议
    if changlun_result and changlun_result.get('recent_fractal'):
        fractal_type = changlun_result['recent_fractal'].get('type')
        if fractal_type == 'top':
            suggestions.append('近期出现顶分型，注意风险')
        elif fractal_type == 'bottom':
            suggestions.append('近期出现底分型，可关注机会')
    
    return suggestions

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    logger.info("启动量化交易分析系统 MVP v1.0")
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )