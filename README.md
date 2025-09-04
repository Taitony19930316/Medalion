# 🏆 Medallion 量化交易系统

[![CI/CD Pipeline](https://github.com/Taitony19930316/Medalion/actions/workflows/ci.yml/badge.svg)](https://github.com/Taitony19930316/Medalion/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)

> 基于缠论技术分析和AI智能增强的专业量化交易系统

## 功能特性

### 核心策略树
- **缠论系统**: 笔段识别、中枢判断、背驰分析
- **技术指标**: MACD、KDJ、RSI、布林带
- **均线系统**: 多周期均线强弱判断
- **强弱分析**: 相对强弱指标、板块轮动
- **趋势信号**: 趋势确认、反转识别
- **量价分析**: 成交量确认信号

### 策略机器人
- 多策略并行执行
- 策略权重动态调整
- 风险分散管理
- 收益最大化算法
- 亏损控制机制

### AI智能模块 🤖
- **策略提炼**: 自动分析历史交易，总结成功模式
- **自然语言策略生成**: 根据文字描述生成可执行策略
- **智能股池筛选**: 基于多维度分析自动筛选标的
- **置信度评估**: 实时评估市场对策略的适配度
- **策略优化建议**: AI驱动的参数调优和策略改进

### 缠论交易体系 📈
- **日线一笔级别**: 专注日线级别的笔段分析
- **六大决策维度**:
  1. **趋势分析**: 确保操作方向与日线笔趋势一致
  2. **相对强弱**: 多维度强弱对比和板块轮动
  3. **相对位置**: 基于历史区间的价格位置判断
  4. **背驰信号**: 识别趋势转折的关键信号
  5. **情绪监控**: 极端超买超卖的及时提醒
  6. **仓位管理**: 不同走势配置差异化仓位

### 策略跟踪复制 👥
- **多平台跟踪**: 支持跟踪不同平台的优秀交易者
- **模式识别**: 自动分析被跟踪者的交易模式
- **智能复制**: 生成可执行的模仿策略代码
- **风险控制**: 跟单信号的验证和冲突检测

## 开发进度

### 基础框架 (第1-2周)
- [ ] 数据获取模块
- [ ] 基础技术指标库
- [ ] 策略基类设计

### 核心策略 (第3-6周)  
- [ ] 缠论算法实现
- [ ] 强弱分析系统
- [ ] 趋势识别算法
- [ ] 多因子信号融合

### 策略机器人 (第7-8周)
- [ ] 多策略管理器
- [ ] 动态权重分配
- [ ] 风险控制引擎

### AI智能模块 (第7-8周)
- [ ] 策略分析器开发
- [ ] NLP策略生成器
- [ ] AI股票筛选器
- [ ] 置信度评估系统
- [ ] AI管理器集成

### 执行与监控 (第9-10周)
- [ ] 自动交易执行
- [ ] 实时监控面板
- [ ] 回测优化系统
- [ ] AI功能界面集成

## 环境要求

- Python 3.8+
- 相关依赖包（见requirements.txt）

## 🎯 核心交易理念

### 缠论日线一笔交易体系

本系统基于缠论理论，专注于日线级别的一笔交易，核心理念如下：

#### 1. 趋势一致性原则
- 确保操作方向与日线笔的趋势方向一致
- 多头趋势中寻找买点，空头趋势中寻找卖点
- 震荡市中以区间操作为主

#### 2. 六维决策框架

**维度一：趋势分析**
- 基于笔段结构判断趋势方向
- 结合多周期均线确认趋势强度
- 识别趋势的延续和转折信号

**维度二：相对强弱**
- 个股与大盘的相对强弱对比
- 板块轮动和资金流向分析
- RSI、CCI等强弱指标综合判断

**维度三：相对位置**
- 当前价格在历史区间中的位置
- 高位谨慎，低位积极的操作策略
- 结合支撑阻力位进行精确定位

**维度四：背驰信号**
- 价格与MACD的背离识别
- 顶背驰和底背驰的确认
- 背驰后的转折时机把握

**维度五：情绪监控**
- RSI极值的超买超卖提醒
- 市场恐慌和贪婪情绪的量化
- 逆向思维的极端情况操作

**维度六：仓位管理**
- 不同信号强度的差异化仓位
- 趋势确认后的加仓策略
- 风险控制的动态调整

#### 3. 买卖点体系

**买点识别**
- 一买：下跌趋势的转折点
- 二买：上涨趋势中的回调买点
- 三买：突破前高后的回调买点

**卖点识别**
- 一卖：上涨趋势的转折点
- 二卖：下跌趋势中的反弹卖点
- 三卖：跌破前低后的反弹卖点

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd quantitative-trading-system

# 安装依赖
pip install -r requirements.txt

# 配置AI模型（可选）
export OPENAI_API_KEY="your-api-key"
```

### 2. 快速体验

```bash
# 运行快速启动脚本
python start_here.py

# 或直接运行完整演示
python examples/complete_trading_system_demo.py
```

### 3. 基础使用

```python
from src.strategies.comprehensive_strategy_manager import ComprehensiveStrategyManager

# 初始化策略管理器
manager = ComprehensiveStrategyManager()

# 分析股票
analysis = manager.analyze_market_with_changlun("000001", market_data)
print(f"交易信号: {analysis['signal']['type']}")
print(f"置信度: {analysis['signal']['confidence']:.2f}")
```

## 📊 使用场景

### 场景1: 日常选股分析
```python
# 1. 获取股票数据
market_data = get_stock_data("000001")

# 2. 缠论分析
analysis = manager.analyze_market_with_changlun("000001", market_data)

# 3. AI增强分析
ai_analysis = manager.get_ai_enhanced_analysis("000001", market_data)

# 4. 综合决策
if analysis['signal']['confidence'] > 0.7:
    print("强烈推荐买入")
```

### 场景2: 策略跟踪
```python
# 1. 添加要跟踪的交易者
trader_info = {
    'trader_id': 'master_001',
    'name': '缠论高手',
    'win_rate': 0.75
}
manager.track_external_strategy(trader_info)

# 2. 更新交易记录
trades = get_trader_trades('master_001')
manager.update_tracked_strategy_trades('master_001', trades)

# 3. 生成跟单策略
copycat_strategy = manager.strategy_tracker.generate_copycat_strategy('master_001')
```

### 场景3: AI策略生成
```python
# 自然语言描述策略
description = """
我想要一个基于缠论三买的策略：
- 当股价突破前高形成三买点时买入
- 结合MACD金叉确认
- 止损5%，止盈15%
"""

# AI生成策略
strategy = manager.ai_manager.generate_strategy_from_description(description)
print(strategy['strategy_name'])
```

## ⚙️ 配置说明

### 基础配置 (config.py)
```python
# 缠论参数
MIN_K_COUNT = 5           # 最小K线数量识别笔
FRACTAL_THRESHOLD = 0.01  # 分型阈值

# 仓位管理
INITIAL_CAPITAL = 100000  # 初始资金
MAX_POSITION_RATIO = 0.3  # 最大单只股票仓位比例
BASE_POSITION = 0.2       # 基础仓位20%

# AI模型配置
AI_MODEL_CONFIG = {
    'type': 'openai',
    'api_key': 'your-api-key',
    'model_name': 'gpt-3.5-turbo'
}
```

### 策略参数调优
```python
# 根据个人风险偏好调整
changlun_strategy = ChangLunStrategy({
    'min_k_for_stroke': 5,      # 笔的最小K线数
    'base_position': 0.15,      # 基础仓位15%
    'max_position': 0.4,        # 最大仓位40%
    'rsi_overbought': 75,       # RSI超买阈值
    'rsi_oversold': 25          # RSI超卖阈值
})
```

## 🔧 高级功能

### 1. 多策略组合
```python
# 创建策略树
strategy_tree = StrategyTree()

# 添加多个策略
strategy_tree.add_strategy(ChangLunStrategy())
strategy_tree.add_strategy(TrendStrategy())
strategy_tree.add_strategy(StrengthStrategy())

# 获取综合信号
composite_signal = strategy_tree.calculate_composite_signal(data)
```

### 2. 实时监控
```python
# 获取实时仪表板数据
dashboard_data = manager.get_real_time_dashboard_data()

# 监控关键指标
for alert in dashboard_data['alerts']:
    if alert['type'] == 'WARNING':
        send_notification(alert['message'])
```

### 3. 回测验证
```python
# 策略回测
backtest_result = run_backtest(
    strategy=changlun_strategy,
    data=historical_data,
    start_date='2023-01-01',
    end_date='2024-01-01'
)

print(f"年化收益率: {backtest_result['annual_return']:.2%}")
print(f"最大回撤: {backtest_result['max_drawdown']:.2%}")
print(f"夏普比率: {backtest_result['sharpe_ratio']:.2f}")
```

## 📈 性能优化

### 1. 数据缓存
- 使用Redis缓存实时行情数据
- 本地SQLite存储历史数据
- 增量更新减少API调用

### 2. 并行计算
- 多线程处理不同股票的分析
- 异步执行AI模型调用
- 批量处理技术指标计算

### 3. 内存管理
- 滑动窗口处理大量历史数据
- 及时清理过期的分析结果
- 优化DataFrame操作

## 🛡️ 风险管理

### 1. 多层风险控制
```python
# 策略层面
max_single_position = 0.3    # 单只股票最大30%仓位
max_total_position = 0.8     # 总仓位最大80%

# 信号层面
min_confidence = 0.6         # 最小置信度要求
signal_timeout = 3600        # 信号有效期1小时

# 执行层面
max_slippage = 0.002         # 最大滑点0.2%
order_timeout = 300          # 订单超时5分钟
```

### 2. 实时风控
```python
# 动态止损
def dynamic_stop_loss(entry_price, current_price, volatility):
    base_stop = 0.05  # 基础止损5%
    volatility_adjust = volatility * 2  # 波动率调整
    return max(base_stop, volatility_adjust)

# 仓位监控
def position_monitor():
    total_exposure = sum(position['value'] for position in positions.values())
    if total_exposure > max_total_exposure:
        trigger_risk_alert("总仓位超限")
```

## 🤝 贡献指南

欢迎贡献代码和建议！

### 开发流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 遵循 PEP 8 Python 代码规范
- 添加必要的注释和文档字符串
- 编写单元测试覆盖新功能
- 更新相关文档

## 📞 支持与反馈

- **文档**: 查看 `docs/` 目录下的详细文档
- **示例**: 参考 `examples/` 目录下的使用示例
- **问题反馈**: 通过 GitHub Issues 报告问题
- **功能建议**: 欢迎提出新功能建议

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

感谢以下开源项目的支持：
- pandas & numpy - 数据处理
- talib - 技术指标计算
- backtrader - 回测框架
- OpenAI - AI能力支持

## 🤝 贡献

我们欢迎各种形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 贡献者

感谢所有为这个项目做出贡献的开发者！

## 📊 项目统计

- **开发语言**: Python 3.8+
- **Web框架**: Flask
- **前端技术**: Bootstrap 5 + Chart.js
- **数据源**: Tushare, AKShare
- **部署方式**: Docker, 传统部署
- **测试覆盖**: 80%+

## 🗺️ 路线图

查看我们的 [开发路线图](DEVELOPMENT_ROADMAP.md) 了解未来计划：

- [x] **迭代1**: 基础数据分析MVP ✅
- [ ] **迭代2**: 完整缠论分析引擎 🚧
- [ ] **迭代3**: AI智能分析模块
- [ ] **迭代4**: 实时监控系统
- [ ] **迭代5**: 策略跟踪复制
- [ ] **迭代6**: 自动交易执行
- [ ] **迭代7**: 回测与优化
- [ ] **迭代8**: 用户体验优化

## 📞 支持

- 📖 [文档](docs/)
- 🐛 [报告问题](https://github.com/Taitony19930316/Medalion/issues)
- 💬 [讨论交流](https://github.com/Taitony19930316/Medalion/discussions)
- ⭐ 如果这个项目对你有帮助，请给我们一个星标！

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) - 查看文件了解详情。

## ⚠️ 免责声明

**本系统仅供学习和研究使用，不构成投资建议。投资有风险，入市需谨慎。**

---

<div align="center">
  <strong>🚀 让量化交易更智能，让投资决策更科学！</strong>
</div>