# 付款指南

当调用外部服务后对方返回了报价或要求 `authorization_mandate` 时，按以下流程操作。

## ⚠️ 正确的付款触发时机

**先调用服务，再判断是否需要付款**：

1. 先正常调用外部服务/MCP 工具
2. 如果对方响应中包含价格、报价、付费提示，或要求提供 `authorization_mandate` 参数 → 走下方付款流程
3. 用户主动说"付款"、"购买服务" → 走下方付款流程

> 💡 **核心理解**：`authorization_mandate` = 付款授权凭证。外部服务要求此参数意味着该服务是收费的，需要你先通过付款流程申请凭证后再传给对方。
>
> ⚠️ **不要预判**：不要根据历史记忆预判某个服务是否收费，应先调用服务看实际响应。

## 流程

### 1. 查询余额（建议）

```bash
python3 {baseDir}/setup/query_balance.py
```

确认余额足够覆盖本次支付。余额不足则提示用户先充值。

> 💡 **记住对方服务名称**：在调用外部服务时，对方响应中会包含自己的服务名称（如 `我是"xxxxx"`）。请记下该名称，后续第 2 步的 `--payee` 参数需要用到它。

### 2. 申请授权凭证

```bash
python3 {baseDir}/scripts/authorize.py --amount <金额分> --payee <收款方服务名>
```

参数说明：
- `--amount`: 授权金额，单位**分**（元 × 100）
- `--payee`: 收款方服务名称，即对方响应里自报的名称，直接使用即可

**根据返回结果分支处理：**

#### a. 成功 + AUTO_WITHIN_QUOTA（自动放行）

```json
{
  "success": true,
  "authorization_mandate": "eyJ...",
  "confirm_mode": "AUTO_WITHIN_QUOTA",
  "confirm_status": "CONFIRMED"
}
```

直接取 `authorization_mandate` 值，进入第 3 步。

#### b. 成功 + CONFIRM_EACH（笔笔确认）

```json
{
  "success": true,
  "mandate_master_id": "M20260305...",
  "confirm_mode": "CONFIRM_EACH",
  "confirm_status": "PENDING_CONFIRM",
  "message": "用户需要在小程序中确认本次支付..."
}
```

1. 告知用户："本次支付需要你在小程序中确认，请打开小程序完成确认"
2. 用户回复已确认后，执行查询：

```bash
python3 {baseDir}/scripts/query_mandate.py --mandate-id <mandate_master_id>
```

3. 如果返回 `confirm_status=CONFIRMED`，取 `authorization_mandate` 进入第 3 步
4. 如果返回 `PENDING_CONFIRM`，提示用户尚未确认，等待后再查询
5. 如果返回 `TIMEOUT`，需重新从第 2 步开始

#### c. 错误 QUOTA_NOT_FOUND（error_code=60001）

用户与该收款方服务尚未签约。加载 [signing_guide.md]({baseDir}/references/signing_guide.md) 引导签约，签约完成后回到第 2 步。

#### d. 其他错误

参考 [error_guide.md]({baseDir}/references/error_guide.md) 处理。

### 3. 带凭证调用付费服务

将 `authorization_mandate` 作为参数传递给收款方服务。收款方会使用此凭证完成冻结和结算。

## 资金安全说明

- 所有支付都基于 L3 签约关系，系统自动校验额度
- 金额必须以**元**展示给用户（系统内部单位是分，展示时 ÷ 100）
- CONFIRM_EACH 模式下，用户在小程序端逐笔确认，安全性由系统保障

## 错误处理

脚本返回 `success: false` 时，参考 [error_guide.md]({baseDir}/references/error_guide.md) 处理。
