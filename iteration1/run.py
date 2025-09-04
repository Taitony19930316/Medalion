#!/usr/bin/env python3
"""
量化交易分析系统 MVP - 启动脚本
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import app
from config import Config

def main():
    """主函数"""
    print("🚀 启动量化交易分析系统 MVP v1.0")
    print("=" * 50)
    
    # 检查环境
    check_environment()
    
    # 创建必要目录
    create_directories()
    
    # 启动应用
    print(f"📊 系统启动中...")
    print(f"🌐 访问地址: http://{Config.HOST}:{Config.PORT}")
    print(f"🔧 调试模式: {'开启' if Config.DEBUG else '关闭'}")
    print("=" * 50)
    
    try:
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG
        )
    except KeyboardInterrupt:
        print("\n👋 系统已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本需要3.8或更高")
        sys.exit(1)
    
    print(f"✅ Python版本: {sys.version.split()[0]}")
    
    # 检查必要的包
    required_packages = ['flask', 'pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}: 未安装")
    
    if missing_packages:
        print(f"\n请安装缺失的包:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)
    
    # 检查数据源配置
    tushare_token = os.getenv('TUSHARE_TOKEN')
    if tushare_token:
        print("✅ Tushare Token: 已配置")
    else:
        print("⚠️  Tushare Token: 未配置 (将使用模拟数据)")
    
    print()

def create_directories():
    """创建必要目录"""
    directories = ['data', 'logs', 'static/uploads']
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 创建目录: {directory}")
    
    print()

if __name__ == '__main__':
    main()