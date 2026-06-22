# 收款指南

当外部 Agent 带着 `authorization_mandate` 请求你的服务时，按以下流程操作。

## 流程

### 1. 确认凭证

确认请求中包含 `authorization_mandate`（一个 JWT 字符串）。
如果没有凭证，告知对方需要先通过 authorize 获取授权凭证。

### 2. 冻结资金

```bash
python3 {baseDir}/scripts/lock.py --mandate <JWT凭证> --amount <金额分>
```

参数说明：
- `--mandate`: 收到的 JWT 授权凭证
- `--amount`: 冻结金额，单位**分**

返回示例：
```json
{
  "success": true,
  "payment_order_id": "BT20260305...",
  "frozen_amount": 500
}
```

冻结成功意味着资金已锁定，可以安全开始执行服务。

### 3. 执行服务

完成请求方要求的服务内容。

### 4. 结算

服务成功完成后：

```bash
python3 {baseDir}/scripts/settle.py --mandate <JWT凭证> --amount <实际金额分>
```

参数说明：
- `--mandate`: 同一个 JWT 凭证
- `--amount`: 实际结算金额，单位**分**（不能超过冻结金额）

返回示例：
```json
{
  "success": true,
  "payment_order_id": "BT20260305...",
  "settled_amount": 500
}
```

### 5. 服务失败处理

如果服务执行失败，**不要调用 settle.py**。冻结的资金会在凭证过期后自动释放回用户。

## 错误处理

脚本返回 `success: false` 时，参考 [error_guide.md]({baseDir}/references/error_guide.md) 处理。
