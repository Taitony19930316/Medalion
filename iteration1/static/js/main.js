// 量化交易分析系统 - 主要JavaScript文件

// 全局变量
let currentSymbol = null;
let analysisData = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
function initializeApp() {
    console.log('量化交易分析系统初始化...');
    
    // 初始化工具提示
    initializeTooltips();
    
    // 初始化事件监听器
    initializeEventListeners();
    
    // 检查系统状态
    checkSystemStatus();
    
    console.log('系统初始化完成');
}

// 初始化工具提示
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 初始化事件监听器
function initializeEventListeners() {
    // 股票代码输入框回车事件
    const symbolInputs = document.querySelectorAll('input[type="text"][placeholder*="股票代码"]');
    symbolInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = this.closest('form');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
        });
        
        // 输入验证
        input.addEventListener('input', function(e) {
            validateStockCode(this);
        });
    });
    
    // 图表标签切换事件
    const chartTabs = document.querySelectorAll('#chartTabs button[data-bs-toggle="tab"]');
    chartTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(e) {
            handleChartTabSwitch(e.target.getAttribute('data-bs-target'));
        });
    });
}

// 验证股票代码
function validateStockCode(input) {
    const value = input.value.trim();
    const isValid = /^[0-9]{6}$/.test(value);
    
    if (value.length > 0 && !isValid) {
        input.classList.add('is-invalid');
        showInputError(input, '请输入6位数字的股票代码');
    } else {
        input.classList.remove('is-invalid');
        hideInputError(input);
    }
    
    return isValid;
}

// 显示输入错误
function showInputError(input, message) {
    let errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        input.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

// 隐藏输入错误
function hideInputError(input) {
    const errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// 处理图表标签切换
function handleChartTabSwitch(target) {
    console.log('切换到图表:', target);
    
    // 这里可以添加图表切换时的特殊处理逻辑
    // 比如重新调整图表大小等
    setTimeout(() => {
        if (window.Chart) {
            Object.values(Chart.instances).forEach(chart => {
                if (chart.canvas.offsetParent !== null) {
                    chart.resize();
                }
            });
        }
    }, 100);
}

// 检查系统状态
function checkSystemStatus() {
    // 模拟系统状态检查
    const statusElements = {
        dataSource: document.querySelector('.status-indicator[data-status="data-source"]'),
        analysisEngine: document.querySelector('.status-indicator[data-status="analysis-engine"]'),
        cacheSystem: document.querySelector('.status-indicator[data-status="cache-system"]')
    };
    
    // 这里可以添加实际的状态检查逻辑
    console.log('系统状态检查完成');
}

// 格式化数字显示
function formatNumber(num, precision = 2) {
    if (typeof num !== 'number') {
        return 'N/A';
    }
    
    if (num >= 1e8) {
        return (num / 1e8).toFixed(1) + '亿';
    } else if (num >= 1e4) {
        return (num / 1e4).toFixed(1) + '万';
    } else {
        return num.toFixed(precision);
    }
}

// 格式化百分比
function formatPercentage(num, precision = 2) {
    if (typeof num !== 'number') {
        return 'N/A';
    }
    
    const sign = num >= 0 ? '+' : '';
    return sign + num.toFixed(precision) + '%';
}

// 获取价格变化的CSS类
function getPriceChangeClass(change) {
    if (change > 0) return 'text-success';
    if (change < 0) return 'text-danger';
    return 'text-muted';
}

// 获取RSI状态
function getRSIStatus(rsi) {
    if (rsi > 80) return { status: 'overbought', class: 'text-danger', text: '超买' };
    if (rsi < 20) return { status: 'oversold', class: 'text-success', text: '超卖' };
    return { status: 'normal', class: 'text-info', text: '正常' };
}

// 显示加载状态
function showLoading(element, message = '加载中...') {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    
    if (element) {
        element.innerHTML = `
            <div class="text-center py-3">
                <div class="spinner-border text-primary mb-2" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div>${message}</div>
            </div>
        `;
    }
}

// 隐藏加载状态
function hideLoading(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    
    if (element) {
        element.innerHTML = '';
    }
}

// 显示错误消息
function showError(message, type = 'danger') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // 插入到页面顶部
    const container = document.querySelector('.container-fluid') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    // 自动消失
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// 显示成功消息
function showSuccess(message) {
    showError(message, 'success');
}

// API调用封装
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API调用失败:', error);
        throw error;
    }
}

// 搜索股票
async function searchStocks(query) {
    try {
        const data = await apiCall(`/api/search_stocks?q=${encodeURIComponent(query)}`);
        return data.results || [];
    } catch (error) {
        console.error('搜索股票失败:', error);
        return [];
    }
}

// 获取股票信息
async function getStockInfo(symbol) {
    try {
        return await apiCall(`/api/stock_info/${symbol}`);
    } catch (error) {
        console.error('获取股票信息失败:', error);
        return null;
    }
}

// 分析股票
async function analyzeStockAPI(symbol) {
    try {
        return await apiCall(`/api/analyze/${symbol}`);
    } catch (error) {
        console.error('分析股票失败:', error);
        throw error;
    }
}

// 复制到剪贴板
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showSuccess('已复制到剪贴板');
        }).catch(err => {
            console.error('复制失败:', err);
        });
    } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showSuccess('已复制到剪贴板');
        } catch (err) {
            console.error('复制失败:', err);
        }
        document.body.removeChild(textArea);
    }
}

// 下载数据为CSV
function downloadCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// 转换数据为CSV格式
function convertToCSV(data) {
    if (!Array.isArray(data) || data.length === 0) {
        return '';
    }
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => {
            const value = row[header];
            return typeof value === 'string' && value.includes(',') ? `"${value}"` : value;
        }).join(','))
    ].join('\n');
    
    return csvContent;
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 本地存储封装
const storage = {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('存储数据失败:', error);
        }
    },
    
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('读取数据失败:', error);
            return defaultValue;
        }
    },
    
    remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('删除数据失败:', error);
        }
    },
    
    clear() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('清空数据失败:', error);
        }
    }
};

// 导出全局函数
window.quantApp = {
    formatNumber,
    formatPercentage,
    getPriceChangeClass,
    getRSIStatus,
    showLoading,
    hideLoading,
    showError,
    showSuccess,
    apiCall,
    searchStocks,
    getStockInfo,
    analyzeStockAPI,
    copyToClipboard,
    downloadCSV,
    debounce,
    throttle,
    storage
};

console.log('量化交易分析系统 JavaScript 加载完成');