# alipay-demo-for-Stress-Testing

对基于 Node.js + Express 复现的、简单的支付宝支付页面“收银台”的压力测试

### 准备

> 需要 node.js 运行环境

下载或clone本项目

安装依赖

```bash
cd alipay-demo-for-Stress-Testing
npm install
```

运行

```bash
node server.js
```

### 测试

使用 JMeter 命令行或GUI 打开测试计划 `JMeter_Test_Plan.jmx`

修改CSV数据文件设置 中 配置.csv文件路径为 `JMeter_test_data.csv` 的路径

根据需求修改数据、参数及配置

最后运行测试计划开始🍐压力测试