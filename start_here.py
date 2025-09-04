#!/usr/bin/env python3
"""
量化交易系统快速启动脚本
帮助用户快速了解和使用系统功能
"""
import os
import sys
from pathlib import Path

def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🤖 智能量化交易系统                        ║
    ║                                                              ║
    ║    集成缠论、MACD技术分析 + AI大模型智能化功能                ║
    ║                                                              ║
    ║    • 策略自动生成  • 智能选股  • 置信度评估                   ║
    ║    • 交易分析     • 风险管理  • 实时监控                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python版本需要3.8或更高")
        return False
    else:
        print(f"✅ Python版本: {python_version.major}.{python_version.minor}")
    
    # 检查必要的包
    required_packages = ['pandas', 'numpy', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n请安装缺失的包: pip install {' '.join(missing_packages)}")
        return False
    
    # 检查AI配置
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("✅ OpenAI API密钥已配置")
    else:
        print("⚠️  OpenAI API密钥未配置 (AI功能将无法使用)")
    
    return True

def show_menu():
    """显示主菜单"""
    menu = """
    📋 请选择要执行的操作:
    
    1. 🚀 快速体验 - 运行AI功能演示
    2. 📊 查看项目结构
    3. 📖 阅读开发指南
    4. ⚙️  环境配置向导
    5. 🧪 运行测试用例
    6. 📈 启动策略回测
    7. 🔧 配置AI模型
    8. ❓ 帮助文档
    9. 🚪 退出
    
    """
    print(menu)

def run_ai_demo():
    """运行AI功能演示"""
    print("🤖 启动AI功能演示...")
    
    # 检查演示文件是否存在
    demo_file = Path("examples/ai_integration_demo.py")
    if demo_file.exists():
        print("正在运行AI功能演示，请稍候...")
        os.system(f"python {demo_file}")
    else:
        print("❌ 演示文件不存在，请检查项目完整性")

def show_project_structure():
    """显示项目结构"""
    structure = """
    📁 项目结构:
    
    量化交易系统/
    ├── 📄 README.md              # 项目说明
    ├── 📄 requirements.txt       # 依赖包列表
    ├── 📄 config.py             # 配置文件
    ├── 📄 start_here.py         # 快速启动脚本
    ├── 📁 src/                  # 源代码目录
    │   ├── 📁 ai/               # AI智能模块 🤖
    │   │   ├── ai_manager.py    # AI管理器
    │   │   ├── strategy_analyzer.py      # 策略分析器
    │   │   ├── nlp_strategy_generator.py # NLP策略生成
    │   │   ├── stock_screener.py         # 智能选股
    │   │   └── confidence_evaluator.py   # 置信度评估
    │   ├── 📁 strategies/       # 策略模块
    │   ├── 📁 data/            # 数据模块
    │   ├── 📁 indicators/      # 技术指标
    │   └── 📁 risk/            # 风险管理
    ├── 📁 examples/            # 使用示例
    ├── 📁 docs/               # 文档目录
    └── 📁 tests/              # 测试用例
    
    🌟 核心AI功能:
    • 策略自动生成: 将文字描述转换为可执行策略
    • 智能选股: AI驱动的股票筛选和评分
    • 交易分析: 自动分析历史交易，提炼成功模式
    • 置信度评估: 实时评估策略适配度和市场环境
    """
    print(structure)

def show_development_guide():
    """显示开发指南"""
    guide_file = Path("docs/development_guide.md")
    if guide_file.exists():
        print("📖 开发指南位置: docs/development_guide.md")
        print("\n主要内容包括:")
        print("• 系统架构设计")
        print("• 开发路线图")
        print("• AI功能详解")
        print("• 使用示例和最佳实践")
        print("• 常见问题解答")
        
        choice = input("\n是否现在打开开发指南? (y/n): ").lower()
        if choice == 'y':
            try:
                with open(guide_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("\n" + "="*60)
                    print(content[:2000] + "..." if len(content) > 2000 else content)
                    print("="*60)
            except Exception as e:
                print(f"❌ 无法打开文件: {e}")
    else:
        print("❌ 开发指南文件不存在")

def setup_environment():
    """环境配置向导"""
    print("⚙️  环境配置向导")
    print("-" * 40)
    
    # 1. 安装依赖
    print("1. 安装Python依赖包")
    install_deps = input("是否现在安装依赖包? (y/n): ").lower()
    if install_deps == 'y':
        print("正在安装依赖包...")
        os.system("pip install -r requirements.txt")
    
    # 2. 配置API密钥
    print("\n2. 配置AI模型API密钥")
    print("支持的模型:")
    print("• OpenAI GPT (推荐)")
    print("• Anthropic Claude")
    print("• 阿里云通义千问")
    print("• 本地模型 (Ollama)")
    
    model_choice = input("选择要配置的模型 (openai/claude/qwen/local): ").lower()
    
    if model_choice == 'openai':
        api_key = input("请输入OpenAI API密钥: ").strip()
        if api_key:
            print(f"export OPENAI_API_KEY='{api_key}'")
            print("请将上述命令添加到你的 ~/.bashrc 或 ~/.zshrc 文件中")
    
    # 3. 创建必要目录
    print("\n3. 创建必要目录")
    directories = ['data', 'logs', 'backtest_results']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ 创建目录: {dir_name}")
    
    print("\n✅ 环境配置完成!")

def configure_ai_model():
    """配置AI模型"""
    print("🔧 AI模型配置")
    print("-" * 40)
    
    print("当前支持的模型:")
    models = {
        '1': ('OpenAI GPT-3.5/4', 'openai'),
        '2': ('Anthropic Claude', 'claude'),
        '3': ('阿里云通义千问', 'qwen'),
        '4': ('本地模型 (Ollama)', 'local')
    }
    
    for key, (name, _) in models.items():
        print(f"{key}. {name}")
    
    choice = input("\n选择模型 (1-4): ").strip()
    
    if choice in models:
        model_name, model_type = models[choice]
        print(f"\n已选择: {model_name}")
        
        # 生成配置代码
        config_code = f"""
# 在 config.py 中更新 AI_MODEL_CONFIG
AI_MODEL_CONFIG = {{
    'type': '{model_type}',
    'api_key': os.getenv('API_KEY'),  # 请设置对应的环境变量
    'model_name': 'gpt-3.5-turbo',   # 根据选择的模型调整
    'temperature': 0.7
}}
"""
        print(config_code)
    else:
        print("❌ 无效选择")

def show_help():
    """显示帮助信息"""
    help_text = """
    ❓ 帮助信息
    
    🚀 快速开始:
    1. 运行 'python start_here.py' 启动向导
    2. 选择 '环境配置向导' 完成初始设置
    3. 配置AI模型API密钥
    4. 运行AI功能演示体验系统能力
    
    📚 学习资源:
    • README.md - 项目概述和功能介绍
    • docs/development_guide.md - 详细开发指南
    • examples/ - 使用示例代码
    
    🤖 AI功能说明:
    • 策略生成: 输入文字描述，自动生成交易策略
    • 智能选股: 基于策略要求筛选股票池
    • 交易分析: 分析历史交易，提供优化建议
    • 置信度评估: 评估策略在当前市场的适配度
    
    🔧 技术支持:
    • 确保Python版本 >= 3.8
    • 安装所有依赖包: pip install -r requirements.txt
    • 配置API密钥以使用AI功能
    
    📞 联系方式:
    • GitHub Issues: 报告问题和建议
    • 文档: 查看详细使用说明
    """
    print(help_text)

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请先解决上述问题")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("请输入选项 (1-9): ").strip()
            
            if choice == '1':
                run_ai_demo()
            elif choice == '2':
                show_project_structure()
            elif choice == '3':
                show_development_guide()
            elif choice == '4':
                setup_environment()
            elif choice == '5':
                print("🧪 测试功能开发中...")
            elif choice == '6':
                print("📈 回测功能开发中...")
            elif choice == '7':
                configure_ai_model()
            elif choice == '8':
                show_help()
            elif choice == '9':
                print("👋 感谢使用量化交易系统，再见!")
                break
            else:
                print("❌ 无效选项，请重新选择")
            
            input("\n按回车键继续...")
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出程序")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()