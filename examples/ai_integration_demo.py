"""
AI功能集成演示
展示如何在量化交易系统中使用AI功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from src.ai.ai_manager import AIManager
from config import Config

def demo_ai_features():
    """演示AI功能"""
    
    print("🤖 量化交易AI功能演示")
    print("=" * 50)
    
    # 初始化AI管理器
    ai_manager = AIManager()
    
    # 检查模块状态
    status = ai_manager.get_module_status()
    print(f"AI模块状态: {status}")
    print()
    
    # 1. 演示策略生成
    print("📝 1. 自然语言策略生成")
    print("-" * 30)
    
    strategy_description = """
    我想要一个基于缠论和MACD的策略：
    - 当股价形成向上笔且MACD金叉时买入
    - 当MACD死叉或价格跌破20日均线时卖出
    - 止损设置为5%，止盈设置为15%
    - 适用于日线级别的A股市场
    """
    
    print(f"策略描述: {strategy_description}")
    
    generated_strategy = ai_manager.generate_strategy_from_description(strategy_description)
    
    if 'error' not in generated_strategy:
        print("✅ 策略生成成功!")
        print(f"策略名称: {generated_strategy.get('strategy_name', 'N/A')}")
        print(f"入场条件: {generated_strategy.get('entry_conditions', [])}")
        print(f"出场条件: {generated_strategy.get('exit_conditions', [])}")
    else:
        print(f"❌ 策略生成失败: {generated_strategy['error']}")
    
    print()
    
    # 2. 演示交易历史分析
    print("📊 2. 交易历史分析")
    print("-" * 30)
    
    # 创建模拟交易数据
    mock_trades = pd.DataFrame({
        'stock': ['000001', '000002', '600036', '000858', '002415'] * 10,
        'entry_date': pd.date_range('2024-01-01', periods=50, freq='D'),
        'exit_date': pd.date_range('2024-01-02', periods=50, freq='D'),
        'entry_price': np.random.uniform(10, 50, 50),
        'exit_price': np.random.uniform(8, 60, 50),
        'profit': np.random.normal(0.02, 0.08, 50),  # 平均2%收益，8%波动
        'strategy': ['缠论MACD策略'] * 50
    })
    
    print(f"分析 {len(mock_trades)} 笔交易记录...")
    
    analysis_result = ai_manager.analyze_trading_history(mock_trades)
    
    if 'error' not in analysis_result:
        print("✅ 分析完成!")
        stats = analysis_result.get('basic_stats', {})
        print(f"胜率: {stats.get('win_rate', 0):.2%}")
        print(f"平均收益: {stats.get('avg_profit', 0):.2%}")
        print(f"盈亏比: {stats.get('profit_factor', 0):.2f}")
        
        recommendations = analysis_result.get('recommendations', [])
        if recommendations:
            print("AI建议:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"  {i}. {rec}")
    else:
        print(f"❌ 分析失败: {analysis_result['error']}")
    
    print()
    
    # 3. 演示股票筛选
    print("🎯 3. AI股票筛选")
    print("-" * 30)
    
    # 模拟股票池和市场数据
    stock_pool = ['000001', '000002', '600036', '000858', '002415', '600519', '000858']
    
    # 创建模拟市场数据
    market_data = {}
    for stock in stock_pool:
        dates = pd.date_range('2024-01-01', periods=60, freq='D')
        prices = np.random.uniform(10, 50, 60)
        prices = pd.Series(prices).cumsum() / 10 + 20  # 模拟价格走势
        
        market_data[stock] = pd.DataFrame({
            'date': dates,
            'open': prices * 0.99,
            'high': prices * 1.02,
            'low': prices * 0.98,
            'close': prices,
            'volume': np.random.uniform(1000000, 10000000, 60)
        })
    
    strategy_requirements = {
        'strategy_type': '缠论MACD策略',
        'timeframe': '日线',
        'risk_tolerance': '中等',
        'expected_return': '10-20%'
    }
    
    print(f"从 {len(stock_pool)} 只股票中筛选...")
    
    screening_result = ai_manager.screen_stocks_intelligently(
        stock_pool, strategy_requirements, market_data
    )
    
    if 'error' not in screening_result:
        print("✅ 筛选完成!")
        filtered_stocks = screening_result.get('filtered_stocks', [])
        print(f"推荐股票: {filtered_stocks}")
        
        confidence_scores = screening_result.get('confidence_scores', {})
        if confidence_scores:
            print("置信度评分:")
            for stock, score in list(confidence_scores.items())[:5]:
                print(f"  {stock}: {score:.2f}")
    else:
        print(f"❌ 筛选失败: {screening_result['error']}")
    
    print()
    
    # 4. 演示置信度评估
    print("🎯 4. 策略置信度评估")
    print("-" * 30)
    
    strategy_name = "缠论MACD策略"
    recent_signals = mock_trades.tail(20)
    market_indicators = {
        'volatility': 0.025,
        'trend_strength': 0.65,
        'sentiment': 0.7
    }
    
    print(f"评估策略: {strategy_name}")
    
    confidence_result = ai_manager.evaluate_strategy_confidence(
        strategy_name, market_data, recent_signals, market_indicators
    )
    
    if 'error' not in confidence_result:
        print("✅ 评估完成!")
        print(f"综合置信度: {confidence_result.get('overall_confidence', 0):.2f}")
        print(f"投资建议: {confidence_result.get('recommendation', 'N/A')}")
        print(f"风险等级: {confidence_result.get('risk_level', 'N/A')}")
        print(f"建议仓位: {confidence_result.get('suggested_position_size', 0):.1%}")
    else:
        print(f"❌ 评估失败: {confidence_result['error']}")
    
    print()
    
    # 5. 综合AI洞察
    print("🧠 5. AI综合洞察")
    print("-" * 30)
    
    insights = ai_manager.get_ai_insights(
        trades_df=mock_trades,
        market_data=market_data,
        strategy_name=strategy_name
    )
    
    print("✅ 综合分析完成!")
    recommendations = insights.get('recommendations', [])
    if recommendations:
        print("AI综合建议:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    print("\n🎉 AI功能演示完成!")

def demo_batch_strategy_generation():
    """演示批量策略生成"""
    
    print("\n📚 批量策略生成演示")
    print("=" * 50)
    
    ai_manager = AIManager()
    
    strategy_ideas = [
        "基于RSI超买超卖的反转策略",
        "双均线金叉死叉趋势跟踪策略", 
        "布林带突破策略",
        "成交量价格确认策略"
    ]
    
    print(f"批量生成 {len(strategy_ideas)} 个策略...")
    
    results = ai_manager.batch_process_strategies(strategy_ideas)
    
    for i, result in enumerate(results, 1):
        print(f"\n策略 {i}:")
        print(f"原始描述: {result.get('original_description', '')}")
        
        if 'error' not in result:
            print(f"生成的策略名: {result.get('strategy_name', 'N/A')}")
            print("✅ 生成成功")
        else:
            print(f"❌ 生成失败: {result['error']}")

if __name__ == "__main__":
    # 设置环境变量（演示用）
    os.environ['OPENAI_API_KEY'] = 'your-api-key-here'  # 请替换为实际的API密钥
    
    try:
        demo_ai_features()
        demo_batch_strategy_generation()
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        print("请检查AI模型配置和API密钥设置")