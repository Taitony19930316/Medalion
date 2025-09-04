#!/bin/bash

# GitHub部署脚本

set -e

echo "🚀 Medallion量化交易系统 - GitHub部署脚本"
echo "============================================"

# 检查Git状态
if [ -d ".git" ]; then
    echo "✅ Git仓库已存在"
else
    echo "📝 初始化Git仓库..."
    git init
    git branch -M main
fi

# 添加远程仓库
REPO_URL="https://github.com/Taitony19930316/Medalion.git"
if git remote get-url origin > /dev/null 2>&1; then
    echo "✅ 远程仓库已配置"
else
    echo "🔗 添加远程仓库..."
    git remote add origin $REPO_URL
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 提交更改..."
    git add .
    git commit -m "feat: 初始化Medallion量化交易系统

- 完成迭代1 MVP版本
- 基础数据分析功能
- 缠论技术分析
- Web界面和API
- Docker部署支持
- 完整的测试覆盖"
else
    echo "✅ 没有未提交的更改"
fi

# 推送到GitHub
echo "🚀 推送到GitHub..."
git push -u origin main

echo ""
echo "🎉 部署完成!"
echo "📖 项目地址: https://github.com/Taitony19930316/Medalion"
echo "📋 下一步:"
echo "  1. 在GitHub上查看项目"
echo "  2. 设置GitHub Pages（如需要）"
echo "  3. 配置GitHub Actions"
echo "  4. 邀请协作者"