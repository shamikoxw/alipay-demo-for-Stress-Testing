// server.js - 支付宝收银台模拟后端
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();

// 中间件配置
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// 模拟数据库
const orders = new Map();
const payments = new Map();

// 生成订单ID
function generateOrderId() {
  return `ORDER${Date.now()}${Math.random().toString(36).substr(2, 9)}`;
}

// 路由1: 创建支付订单
app.post('/api/payment/create', (req, res) => {
  const { amount, subject, bankCard } = req.body;
  
  const orderId = generateOrderId();
  const order = {
    orderId,
    amount: amount || 579.00,
    subject: subject || '罗技大师系列MX Master 3s无线蓝牙双模鼠标',
    bankCard: bankCard || '****7061',
    bankName: '中国建设银行',
    status: 'pending',
    createTime: new Date().toISOString()
  };
  
  orders.set(orderId, order);
  
  // 模拟响应时间（50-200ms）
  const delay = Math.random() * 150 + 50;
  setTimeout(() => {
    res.json({
      success: true,
      code: 0,
      data: order,
      message: '订单创建成功'
    });
  }, delay);
});

// 路由2: 获取支付页面信息
app.get('/api/payment/info/:orderId', (req, res) => {
  const { orderId } = req.params;
  const order = orders.get(orderId);
  
  if (!order) {
    return res.status(404).json({
      success: false,
      code: 404,
      message: '订单不存在'
    });
  }
  
  // 模拟响应时间
  const delay = Math.random() * 100 + 30;
  setTimeout(() => {
    res.json({
      success: true,
      code: 0,
      data: order
    });
  }, delay);
});

// 路由3: 提交支付密码（核心接口）
app.post('/api/payment/validate', (req, res) => {
  const { orderId, password } = req.body;
  
  const order = orders.get(orderId);
  
  if (!order) {
    return res.status(404).json({
      success: false,
      code: 404,
      message: '订单不存在'
    });
  }
  
  // 模拟密码验证（测试密码: 123456）
  const isValidPassword = password === '123456';
  
  // 模拟5%的失败率
  const randomFail = Math.random() < 0.05;
  
  // 模拟响应时间（100-500ms）
  const delay = Math.random() * 400 + 100;
  
  setTimeout(() => {
    if (randomFail || !isValidPassword) {
      res.json({
        success: false,
        code: 1001,
        message: '支付密码错误',
        data: null
      });
    } else {
      order.status = 'success';
      order.payTime = new Date().toISOString();
      
      const payment = {
        paymentId: `PAY${Date.now()}`,
        orderId,
        amount: order.amount,
        status: 'success',
        payTime: order.payTime
      };
      
      payments.set(payment.paymentId, payment);
      
      res.json({
        success: true,
        code: 0,
        message: '支付成功',
        data: payment
      });
    }
  }, delay);
});

// 路由4: 查询支付结果
app.get('/api/payment/query/:orderId', (req, res) => {
  const { orderId } = req.params;
  const order = orders.get(orderId);
  
  if (!order) {
    return res.status(404).json({
      success: false,
      code: 404,
      message: '订单不存在'
    });
  }
  
  const delay = Math.random() * 80 + 20;
  setTimeout(() => {
    res.json({
      success: true,
      code: 0,
      data: {
        orderId: order.orderId,
        status: order.status,
        amount: order.amount,
        payTime: order.payTime
      }
    });
  }, delay);
});

// 路由5: 安全检测接口
app.get('/api/security/check', (req, res) => {
  // 模拟安全检测
  const delay = Math.random() * 50 + 10;
  setTimeout(() => {
    res.json({
      success: true,
      code: 0,
      message: '安全设置检测成功！',
      data: {
        deviceCheck: true,
        riskLevel: 'low'
      }
    });
  }, delay);
});

// 统计接口（用于监控）
app.get('/api/stats', (req, res) => {
  res.json({
    totalOrders: orders.size,
    totalPayments: payments.size,
    successRate: payments.size / Math.max(orders.size, 1)
  });
});

// 启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`支付宝收银台模拟服务器运行在端口 ${PORT}`);
  console.log(`访问 http://localhost:${PORT} 进行测试`);
});

// 导出供测试使用
module.exports = app;