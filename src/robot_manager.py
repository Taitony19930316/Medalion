"""
策略机器人管理器 - 多策略并行执行和管理
"""
from typing import Dict, List, Optional
import pandas as pd
import threading
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from .strategies.strategy_tree import StrategyTree
from .strategies.base_strategy import TradingSignal, SignalType

class RobotStatus(Enum):
    """机器人状态"""
    STOPPED = "停止"
    RUNNING = "运行中"
    PAUSED = "暂停"
    ERROR = "错误"

@dataclass
class RobotConfig:
    """机器人配置"""
    name: str
    symbols: List[str]  # 交易标的
    max_positions: int = 5  # 最大持仓数
    capital_allocation: float = 0.2  # 资金分配比例
    risk_level: float = 0.05  # 风险水平
    update_interval: int = 60  # 更新间隔(秒)

class TradingRobot:
    """单个交易机器人"""
    
    def __init__(self, config: RobotConfig, strategy_tree: StrategyTree):
        self.config = config
        self.strategy_tree = strategy_tree
        self.status = RobotStatus.STOPPED
        self.positions: Dict[str, Dict] = {}  # 持仓信息
        self.performance_metrics = {
            'total_pnl': 0.0,
            'win_rate': 0.0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0,
            'trade_count': 0
        }
        self.last_update = None
        self.error_message = ""
        
    def start(self):
        """启动机器人"""
        self.status = RobotStatus.RUNNING
        self.error_message = ""
        
    def stop(self):
        """停止机器人"""
        self.status = RobotStatus.STOPPED
        
    def pause(self):
        """暂停机器人"""
        self.status = RobotStatus.PAUSED
        
    def process_signals(self, market_data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """
        处理交易信号
        Args:
            market_data: {symbol: DataFrame} 市场数据
        Returns:
            交易指令列表
        """
        if self.status != RobotStatus.RUNNING:
            return []
            
        orders = []
        
        try:
            for symbol in self.config.symbols:
                if symbol not in market_data:
                    continue
                    
                data = market_data[symbol]
                signal = self.strategy_tree.calculate_composite_signal(data)
                
                if signal:
                    order = self._generate_order(symbol, signal, data)
                    if order:
                        orders.append(order)
                        
            self.last_update = datetime.now()
            
        except Exception as e:
            self.status = RobotStatus.ERROR
            self.error_message = str(e)
            
        return orders
    
    def _generate_order(self, symbol: str, signal: TradingSignal, data: pd.DataFrame) -> Optional[Dict]:
        """根据信号生成订单"""
        current_price = data.iloc[-1]['close']
        
        # 检查是否已有持仓
        current_position = self.positions.get(symbol, {})
        
        if signal.signal_type == SignalType.BUY:
            # 买入信号
            if not current_position:  # 无持仓时买入
                position_size = self._calculate_position_size(current_price, signal.confidence)
                return {
                    'symbol': symbol,
                    'action': 'BUY',
                    'quantity': position_size,
                    'price': current_price,
                    'signal_strength': signal.strength.name,
                    'confidence': signal.confidence,
                    'reason': signal.reason,
                    'robot_name': self.config.name
                }
                
        elif signal.signal_type == SignalType.SELL:
            # 卖出信号
            if current_position:  # 有持仓时卖出
                return {
                    'symbol': symbol,
                    'action': 'SELL',
                    'quantity': current_position.get('quantity', 0),
                    'price': current_price,
                    'signal_strength': signal.strength.name,
                    'confidence': signal.confidence,
                    'reason': signal.reason,
                    'robot_name': self.config.name
                }
                
        return None
    
    def _calculate_position_size(self, price: float, confidence: float) -> int:
        """计算仓位大小"""
        # 基础仓位 = 分配资金 / 价格
        base_size = (self.config.capital_allocation * 100000) / price  # 假设总资金10万
        
        # 根据信号置信度调整
        adjusted_size = base_size * confidence
        
        # 风险控制
        max_size = (self.config.capital_allocation * 100000 * 0.1) / price  # 最大10%资金
        
        return min(int(adjusted_size), int(max_size))
    
    def update_position(self, symbol: str, action: str, quantity: int, price: float):
        """更新持仓"""
        if action == 'BUY':
            self.positions[symbol] = {
                'quantity': quantity,
                'avg_price': price,
                'entry_time': datetime.now()
            }
        elif action == 'SELL':
            if symbol in self.positions:
                # 计算盈亏
                entry_price = self.positions[symbol]['avg_price']
                pnl = (price - entry_price) * quantity
                self.performance_metrics['total_pnl'] += pnl
                self.performance_metrics['trade_count'] += 1
                
                # 移除持仓
                del self.positions[symbol]

class RobotManager:
    """机器人管理器"""
    
    def __init__(self):
        self.robots: Dict[str, TradingRobot] = {}
        self.is_running = False
        self.update_thread = None
        
    def add_robot(self, robot: TradingRobot):
        """添加机器人"""
        self.robots[robot.config.name] = robot
        
    def remove_robot(self, robot_name: str):
        """移除机器人"""
        if robot_name in self.robots:
            self.robots[robot_name].stop()
            del self.robots[robot_name]
            
    def start_all_robots(self):
        """启动所有机器人"""
        for robot in self.robots.values():
            robot.start()
        self.is_running = True
        
    def stop_all_robots(self):
        """停止所有机器人"""
        for robot in self.robots.values():
            robot.stop()
        self.is_running = False
        
    def get_robot_status(self) -> Dict:
        """获取所有机器人状态"""
        status = {}
        for name, robot in self.robots.items():
            status[name] = {
                'status': robot.status.value,
                'positions': len(robot.positions),
                'performance': robot.performance_metrics,
                'last_update': robot.last_update,
                'error': robot.error_message
            }
        return status
    
    def process_market_data(self, market_data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """处理市场数据，生成所有机器人的交易指令"""
        all_orders = []
        
        for robot in self.robots.values():
            if robot.status == RobotStatus.RUNNING:
                orders = robot.process_signals(market_data)
                all_orders.extend(orders)
                
        return all_orders
    
    def optimize_all_strategies(self):
        """优化所有机器人的策略权重"""
        for robot in self.robots.values():
            robot.strategy_tree.optimize_weights()