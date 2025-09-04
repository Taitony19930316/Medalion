"""
完整交易体系演示
展示缠论+AI+策略跟踪的综合应用
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.strategies.comprehensive_strategy_manager import ComprehensiveStrategyManager
from config import Config

def create_mock_market_data(symbol: str, days: int = 120) -> pd.DataFrame:
    """创建模拟市场数据"""
    
    # 生成日期序列
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                         periods=days, freq='D')
    
    # 生成价格数据（模拟真实走势）
    np.random.seed(42)  # 固定随机种子，确保结果可重现
    
    # 基础价格趋势
    base_price = 20.0
    trend = np.cumsum(np.random.normal(0.001, 0.02, days))  # 轻微上涨趋势
    prices = base_price * (1 + trend)
    
    # 添加一些技术形态
    # 在第30-40天添加一个明显的上涨笔
    prices[30:40] *= np.linspace(1.0, 1.15, 10)
    
    # 在第60-70天添加一个回调
    prices[60:70] *= np.linspace(1.0, 0.92, 10)
    
    # 在第90-100天添加一个突破
    prices[90:100] *= np.linspace(1.0, 1.20, 10)
    
    # 生成OHLC数据
    data = []
    for i, price in enumerate(prices):
        # 添加日内波动
        daily_volatility = np.random.uniform(0.01, 0.03)
        high = price * (1 + daily_volatility)
        low = price * (1 - daily_volatility)
        open_price = price * np.random.uniform(0.99, 1.01)
        close = price
        
        # 成交量（价格上涨时成交量放大）
        volume_base = 1000000
        if i > 0:
            price_change = (price - prices[i-1]) / prices[i-1]
            volume_multiplier = 1 + abs(price_change) * 5
        else:
            volume_multiplier = 1
        
        volume = int(volume_base * volume_multiplier * np.random.uniform(0.5, 2.0))
        
        data.append({
            'date': dates[i],
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    
    # 计算技术指标
    df = add_technical_indicators(df)
    
    return df

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """添加技术指标"""
    
    # 移动平均线
    df['MA_5'] = df['close'].rolling(window=5).mean()
    df['MA_20'] = df['close'].rolling(window=20).mean()
    df['MA_60'] = df['close'].rolling(window=60).mean()
    
    # MACD
    exp1 = df['close'].ewm(span=12).mean()
    exp2 = df['close'].ewm(span=26).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

def create_mock_trading_history() -> pd.DataFrame:
    """创建模拟交易历史"""
    
    trades = []
    symbols = ['000001', '000002', '600036', '000858', '002415']
    
    for i in range(50):
        symbol = np.random.choice(symbols)
        entry_date = datetime.now() - timedelta(days=np.random.randint(1, 60))
        exit_date = entry_date + timedelta(days=np.random.randint(1, 10))
        
        entry_price = np.random.uniform(15, 50)
        # 模拟有一定胜率的交易
        if np.random.random() < 0.65:  # 65%胜率
            exit_price = entry_price * np.random.uniform(1.02, 1.15)
        else:
            exit_price = entry_price * np.random.uniform(0.85, 0.98)
        
        profit = (exit_price - entry_price) / entry_price
        
        trades.append({
            'symbol': symbol,
            'entry_date': entry_date,
            'exit_date': exit_date,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'profit': profit,
            'strategy': '缠论策略'
        })
    
    return pd.DataFrame(trades)

def demo_complete_trading_system():
    """演示完整交易体系"""
    
    print("🚀 完整量化交易体系演示")
    print("=" * 60)
    
    # 初始化综合策略管理器
    ai_config = Config.AI_MODEL_CONFIG if hasattr(Config, 'AI_MODEL_CONFIG') else None
    manager = ComprehensiveStrategyManager(ai_config)
    
    print("✅ 策略管理器初始化完成")
    print(f"   - 缠论策略: 已启用")
    print(f"   - AI功能: {'已启用' if manager.ai_manager else '未启用'}")
    print(f"   - 策略跟踪: 已启用")
    print()
    
    # 1. 缠论市场分析演示
    print("📊 1. 缠论市场分析")
    print("-" * 40)
    
    # 创建模拟数据
    symbol = "000001"
    market_data = create_mock_market_data(symbol, 120)
    
    print(f"分析股票: {symbol}")
    print(f"数据周期: {len(market_data)} 个交易日")
    
    # 进行缠论分析
    changlun_analysis = manager.analyze_market_with_changlun(symbol, market_data)
    
    print("\n缠论分析结果:")
    signal = changlun_analysis['signal']
    market_analysis = changlun_analysis['market_analysis']
    
    print(f"  交易信号: {signal['type']}")
    print(f"  信号强度: {signal['strength']}")
    print(f"  置信度: {signal['confidence']:.2f}")
    print(f"  建议仓位: {signal['suggested_position']:.1%}")
    print(f"  信号原因: {signal['reason']}")
    
    print(f"\n市场状态:")
    print(f"  趋势方向: {market_analysis['trend_direction']}")
    print(f"  相对位置: {market_analysis['relative_position']}")
    print(f"  RSI值: {market_analysis['rsi_value']:.1f}")
    print(f"  背驰信号: {market_analysis['divergence_signal'] or '无'}")
    print(f"  情绪极端: {'是' if market_analysis['emotion_extreme'] else '否'}")
    
    print()
    
    # 2. AI增强分析演示
    print("🤖 2. AI增强分析")
    print("-" * 40)
    
    # 创建模拟交易历史
    trading_history = create_mock_trading_history()
    
    if manager.ai_manager:
        print("正在进行AI增强分析...")
        
        ai_analysis = manager.get_ai_enhanced_analysis(
            symbol, market_data, trading_history
        )
        
        if 'error' not in ai_analysis:
            print("✅ AI分析完成!")
            
            # AI置信度评估
            ai_confidence = ai_analysis['ai_confidence']
            print(f"\nAI置信度评估:")
            print(f"  综合置信度: {ai_confidence.get('overall_confidence', 0):.2f}")
            print(f"  投资建议: {ai_confidence.get('recommendation', 'N/A')}")
            print(f"  风险等级: {ai_confidence.get('risk_level', 'N/A')}")
            
            # 增强推荐
            enhanced_rec = ai_analysis['enhanced_recommendation']
            print(f"\n增强推荐:")
            print(f"  最终建议: {enhanced_rec['recommendation']}")
            print(f"  建议操作: {enhanced_rec['action']}")
            print(f"  综合评分: {enhanced_rec['combined_confidence']:.2f}")
            print(f"  建议仓位: {enhanced_rec['suggested_position_size']:.1%}")
            
            print(f"\n推理过程:")
            for reason in enhanced_rec['reasoning']:
                print(f"    • {reason}")
        else:
            print(f"❌ AI分析失败: {ai_analysis['error']}")
    else:
        print("⚠️  AI功能未启用，跳过AI分析")
    
    print()
    
    # 3. 策略跟踪演示
    print("👥 3. 策略跟踪演示")
    print("-" * 40)
    
    # 添加一个模拟的优秀交易者
    trader_info = {
        'trader_id': 'master_trader_001',
        'name': '缠论大师',
        'platform': '东方财富',
        'win_rate': 0.72,
        'total_return': 0.35,
        'max_drawdown': 0.08
    }
    
    track_result = manager.track_external_strategy(trader_info)
    print(f"✅ {track_result}")
    
    # 模拟该交易者的一些交易记录
    mock_trades = [
        {
            'symbol': '000001',
            'action': 'BUY',
            'price': 25.50,
            'quantity': 1000,
            'timestamp': datetime.now() - timedelta(hours=2),
            'profit_loss_ratio': 0.05
        },
        {
            'symbol': '600036',
            'action': 'SELL',
            'price': 42.30,
            'quantity': 800,
            'timestamp': datetime.now() - timedelta(hours=1),
            'profit_loss_ratio': 0.08
        }
    ]
    
    manager.update_tracked_strategy_trades('master_trader_001', mock_trades)
    print(f"✅ 已更新交易记录 {len(mock_trades)} 笔")
    
    # 获取跟踪表现
    tracking_performance = manager.strategy_tracker.get_tracker_performance()
    print(f"\n跟踪统计:")
    print(f"  跟踪交易者数量: {tracking_performance['total_tracked_traders']}")
    print(f"  活跃交易者: {tracking_performance['active_traders']}")
    print(f"  总跟踪交易数: {tracking_performance['total_trades_tracked']}")
    
    print()
    
    # 4. 综合决策演示
    print("🎯 4. 综合决策系统")
    print("-" * 40)
    
    print("整合所有信号源进行综合决策...")
    
    # 这里可以展示如何整合缠论信号、AI分析和跟踪信号
    final_decision = {
        'symbol': symbol,
        'changlun_signal': signal['type'],
        'changlun_confidence': signal['confidence'],
        'ai_recommendation': enhanced_rec['recommendation'] if manager.ai_manager else 'N/A',
        'tracking_signals': len(manager.recent_signals),
        'final_action': 'BUY' if signal['confidence'] > 0.6 else 'HOLD',
        'position_size': min(signal['suggested_position'], 0.2)  # 最大20%仓位
    }
    
    print(f"\n综合决策结果:")
    print(f"  标的: {final_decision['symbol']}")
    print(f"  缠论信号: {final_decision['changlun_signal']} (置信度: {final_decision['changlun_confidence']:.2f})")
    print(f"  AI建议: {final_decision['ai_recommendation']}")
    print(f"  跟踪信号数: {final_decision['tracking_signals']}")
    print(f"  最终决策: {final_decision['final_action']}")
    print(f"  建议仓位: {final_decision['position_size']:.1%}")
    
    print()
    
    # 5. 每日报告演示
    print("📋 5. 每日策略报告")
    print("-" * 40)
    
    daily_report = manager.generate_daily_strategy_report()
    
    print(f"报告日期: {daily_report['date']}")
    print(f"\n概要:")
    summary = daily_report['summary']
    print(f"  策略数量: {summary['total_strategies']}")
    print(f"  活跃持仓: {summary['active_positions']}")
    print(f"  今日信号: {summary['signals_generated']}")
    
    print(f"\n今日建议:")
    for i, rec in enumerate(daily_report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print()
    
    # 6. 实时仪表板数据
    print("📊 6. 实时仪表板")
    print("-" * 40)
    
    dashboard_data = manager.get_real_time_dashboard_data()
    
    print(f"更新时间: {dashboard_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"市场状态: {dashboard_data['market_status']}")
    print(f"当前持仓: {dashboard_data['current_positions']}")
    
    print(f"\n策略状态:")
    for strategy, status in dashboard_data['strategy_status'].items():
        print(f"  {strategy}: {status}")
    
    print(f"\n最近信号: {len(dashboard_data['recent_signals'])} 个")
    
    print()
    
    # 7. 配置导出
    print("⚙️  7. 策略配置")
    print("-" * 40)
    
    config = manager.export_strategy_config()
    
    print("当前配置:")
    print(f"  缠论策略: {'启用' if config['changlun_strategy']['enabled'] else '禁用'}")
    print(f"  AI功能: {'启用' if config['ai_features']['enabled'] else '禁用'}")
    print(f"  策略跟踪: {'启用' if config['strategy_tracking']['enabled'] else '禁用'}")
    print(f"  最大持仓数: {config['risk_management']['max_positions']}")
    print(f"  总资金: {config['risk_management']['total_capital']:,}")
    
    print("\n🎉 完整交易体系演示完成!")
    print("\n💡 系统特色:")
    print("   ✓ 基于缠论的日线一笔级别分析")
    print("   ✓ 六大维度综合决策 (趋势/强弱/位置/背驰/情绪/仓位)")
    print("   ✓ AI增强的策略分析和优化")
    print("   ✓ 策略跟踪和复制功能")
    print("   ✓ 多策略融合决策")
    print("   ✓ 完整的风险管理体系")

def demo_strategy_customization():
    """演示策略自定义功能"""
    
    print("\n🔧 策略自定义演示")
    print("=" * 60)
    
    # 演示如何根据用户需求调整策略参数
    print("根据你的交易体系，可以自定义以下参数:")
    
    customization_options = {
        '缠论参数': {
            '最小笔K线数': '5 (可调整为3-10)',
            '分型识别阈值': '0.01 (可调整为0.005-0.02)',
            '趋势判断周期': '[5,20,60] (可自定义均线组合)'
        },
        '仓位管理': {
            '基础仓位': '20% (可调整为10%-30%)',
            '最大仓位': '50% (可调整为30%-80%)',
            '单股最大仓位': '30% (可调整为20%-50%)'
        },
        '风险控制': {
            'RSI超买阈值': '80 (可调整为70-90)',
            'RSI超卖阈值': '20 (可调整为10-30)',
            '背驰确认强度': '中等 (可选择宽松/中等/严格)'
        },
        'AI增强': {
            '置信度权重': '缠论40% + AI40% + 筛选20%',
            '信号过滤阈值': '0.6 (可调整为0.4-0.8)',
            '模型选择': 'GPT/Claude/通义千问/本地模型'
        }
    }
    
    for category, options in customization_options.items():
        print(f"\n{category}:")
        for param, description in options.items():
            print(f"  • {param}: {description}")
    
    print(f"\n📝 个性化建议:")
    print(f"  1. 根据你的风险偏好调整仓位管理参数")
    print(f"  2. 根据交易频率调整信号灵敏度")
    print(f"  3. 根据市场环境动态调整AI权重")
    print(f"  4. 定期回测优化参数设置")

if __name__ == "__main__":
    try:
        demo_complete_trading_system()
        demo_strategy_customization()
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("请检查依赖包安装和配置设置")