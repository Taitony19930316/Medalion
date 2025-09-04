# 迭代1: 基础数据分析MVP

## 🎯 迭代目标

构建一个**最小可用的股票技术分析系统**，用户可以输入股票代码，查看K线图和基础技术指标。

## 📋 功能清单

### 核心功能
- [x] 股票数据获取（支持A股主要股票）
- [x] 基础技术指标计算（MA、MACD、RSI）
- [x] 简单分型识别
- [x] Web界面展示
- [x] 图表可视化

### 技术特性
- [x] 数据缓存机制
- [x] 错误处理
- [x] 响应式设计
- [x] Docker部署

## 🏗️ 系统架构

```
用户浏览器
    ↓
Flask Web应用
    ↓
数据获取模块 → 技术指标计算 → 缠论分析
    ↓
SQLite数据库 ← → 外部API (tushare/akshare)
```

## 📁 项目结构

```
iteration1/
├── app.py                 # Flask主应用
├── config.py             # 配置文件
├── requirements.txt      # 依赖包
├── Dockerfile           # Docker配置
├── data/
│   ├── fetcher.py       # 数据获取
│   ├── indicators.py    # 技术指标
│   └── changlun.py      # 缠论分析
├── templates/
│   ├── index.html       # 主页面
│   └── analysis.html    # 分析页面
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── tests/               # 测试文件
```

## 🚀 快速开始

### 方式一：直接运行（推荐开发）
```bash
# 1. 进入项目目录
cd iteration1

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量（可选）
cp .env.example .env
# 编辑 .env 文件，添加 Tushare Token 等配置

# 4. 启动应用
python run.py
```

### 方式二：Docker部署（推荐生产）
```bash
# 1. 进入项目目录
cd iteration1

# 2. 快速部署
./deploy.sh

# 或手动部署
docker-compose up -d
```

### 方式三：开发模式
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 直接启动Flask应用
python app.py
```

### 4. 访问系统
- 开发模式: http://localhost:5000
- Docker部署: http://localhost:5000

## 📊 使用示例

1. 在首页输入股票代码（如：000001）
2. 点击"分析"按钮
3. 查看K线图和技术指标
4. 观察分型标注点

## 🧪 测试验证

### 功能测试
```bash
# 运行单元测试
python -m pytest tests/

# 测试数据获取
python tests/test_data_fetcher.py

# 测试技术指标
python tests/test_indicators.py
```

### 性能测试
- 单次查询响应时间 < 3秒
- 支持并发用户数 > 10
- 内存使用 < 500MB

## 📦 部署方案

### Docker部署
```bash
# 构建镜像
docker build -t quant-mvp:v1.0 .

# 运行容器
docker run -p 5000:5000 quant-mvp:v1.0
```

### 云服务部署
支持部署到：
- 阿里云ECS
- 腾讯云CVM
- AWS EC2
- 本地服务器

## 📈 成功标准

### 功能验证
- ✅ 能获取A股主要股票数据
- ✅ 正确计算技术指标
- ✅ 识别基础分型点
- ✅ 图表展示清晰

### 性能要求
- ✅ 响应时间 < 3秒
- ✅ 系统稳定运行
- ✅ 错误处理完善
- ✅ 用户体验良好

## 🔄 下个迭代预告

迭代2将在此基础上增加：
- 完整的缠论笔段识别
- 买卖点标注
- 趋势判断
- 更丰富的可视化

## 🛠️ 开发指南

### 项目结构说明
```
iteration1/
├── app.py              # Flask主应用
├── config.py           # 配置文件
├── run.py             # 启动脚本
├── requirements.txt    # Python依赖
├── Dockerfile         # Docker配置
├── docker-compose.yml # Docker Compose配置
├── deploy.sh          # 部署脚本
├── data/              # 数据模块
│   ├── fetcher.py     # 数据获取
│   ├── indicators.py  # 技术指标
│   └── changlun.py    # 缠论分析
├── templates/         # HTML模板
├── static/           # 静态文件
└── tests/            # 测试文件
```

### 添加新功能
1. 在对应模块中添加功能代码
2. 在 `app.py` 中添加API路由
3. 在模板中添加前端界面
4. 编写测试用例

### 运行测试
```bash
# 安装测试依赖
pip install pytest pytest-flask

# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_app.py
```

## 📊 API文档

### 分析股票
```
GET /api/analyze/<symbol>
```
返回股票的完整技术分析结果。

### 获取股票信息
```
GET /api/stock_info/<symbol>
```
返回股票基本信息。

### 搜索股票
```
GET /api/search_stocks?q=<query>
```
根据关键词搜索股票。

## 🔧 配置说明

### 环境变量
- `TUSHARE_TOKEN`: Tushare API密钥（可选）
- `FLASK_ENV`: Flask环境（development/production）
- `DEBUG`: 调试模式开关
- `HOST`: 服务器地址
- `PORT`: 服务器端口

### 数据源配置
系统支持多种数据源：
1. **Tushare**: 需要注册获取Token
2. **AKShare**: 免费开源数据源
3. **模拟数据**: 用于演示和测试

## 📞 问题反馈

### 常见问题
1. **数据获取失败**: 检查网络连接和API配置
2. **页面加载慢**: 可能是首次获取数据，请耐心等待
3. **图表不显示**: 检查浏览器JavaScript是否启用
4. **Docker启动失败**: 检查端口是否被占用

### 日志查看
```bash
# 查看应用日志
tail -f logs/app.log

# 查看Docker日志
docker-compose logs -f
```

### 获取帮助
- 查看项目文档
- 检查测试用例
- 提交Issue反馈问题