#!/bin/bash

# 量化交易分析系统 MVP - 快速部署脚本

set -e

echo "🚀 量化交易分析系统 MVP 部署脚本"
echo "=================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

echo "✅ Docker环境检查通过"

# 创建必要目录
echo "📁 创建必要目录..."
mkdir -p data logs

# 复制环境变量文件
if [ ! -f .env ]; then
    echo "📝 创建环境变量文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件，配置必要的环境变量"
fi

# 构建和启动服务
echo "🔨 构建Docker镜像..."
docker-compose build

echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ 服务启动成功!"
    echo "🌐 访问地址: http://localhost:5000"
else
    echo "❌ 服务启动失败，请检查日志:"
    docker-compose logs
    exit 1
fi

echo ""
echo "🎉 部署完成!"
echo ""
echo "📋 常用命令:"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo "  查看状态: docker-compose ps"
echo ""
echo "📖 更多信息请查看 README.md"