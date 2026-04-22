# 错误处理指南

当工具调用返回 `success: false` 时，根据 `error_code` 查找处理方式。

## 认证类错误

### KYA_VERIFICATION_FAILED
**含义：** Agent 身份验证失败
**用户提示：** "支付服务暂时不可用，请检查配置"
**处理：** 检查 mcp-server/config.json 中的 agent_did 和密钥文件是否正确

### SIGNATURE_INVALID
**含义：** 请求签名验证失败
**用户提示：** "安全验证失败，请重试"
**处理：** 密钥可能损坏，运行 `python {baseDir}/setup/generate_keys.py --force` 重新生成后更新后端公钥

## 签约/额度类错误

### 60001 / QUOTA_NOT_FOUND
**含义：** 用户与该收款方服务未签约 L3 授权关系
**用户提示：** "你还没有与该服务签约授权，需要先完成签约"
**处理：** 加载 [signing_guide.md]({baseDir}/references/signing_guide.md) 引导用户签约

### 60002 / QUOTA_EXPIRED
**含义：** 签约授权已过期
**用户提示：** "签约授权已过期，需要重新签约"
**处理：** 加载 [signing_guide.md]({baseDir}/references/signing_guide.md) 引导用户重新签约

### 60003 / QUOTA_DISABLED
**含义：** 签约授权已关闭
**用户提示：** "该服务的自动授权已关闭，请在小程序中重新开启"
**处理：** 引导用户在小程序中管理签约关系

### 60004 / AMOUNT_EXCEED_QUOTA
**含义：** 金额超过签约额度
**用户提示：** "本次金额超出了你设定的签约额度，请减少金额或在小程序中调整额度"
**处理：** 引导用户减少金额或在小程序中修改签约额度

### 60005 / MANDATE_PENDING_CONFIRM
**含义：** 凭证等待用户确认
**用户提示：** "支付需要你在小程序中确认"
**处理：** 提示用户打开小程序确认，确认后运行 query_mandate.py 查询

### 60006 / MANDATE_CONFIRM_TIMEOUT
**含义：** 凭证确认超时
**用户提示：** "确认超时，需要重新申请"
**处理：** 重新执行 authorize.py

### 60007 / MANDATE_USE_EXHAUSTED
**含义：** 凭证已使用（单次凭证已被消费）
**用户提示：** "该授权凭证已使用，需要重新申请"
**处理：** 重新执行 authorize.py

## 凭证类错误

### MANDATE_INVALID
**含义：** 授权凭证无效（格式错误或被篡改）
**用户提示：** "授权凭证无效，需要重新授权"
**处理：** 重新调用 authorize.py 获取新凭证

### MANDATE_EXPIRED
**含义：** 授权凭证已过期
**用户提示：** "授权已过期，需要重新授权"
**处理：** 重新调用 authorize.py（凭证有效期为10分钟）

### MANDATE_NOT_FOUND
**含义：** 凭证在后端数据库中不存在
**用户提示：** "找不到对应的授权记录，请重新授权"
**处理：** 重新调用 authorize.py

### CALLER_NOT_AUTHORIZED
**含义：** 当前 Agent 无权使用此凭证
**用户提示：** "你没有使用这个授权凭证的权限"
**处理：** 确认凭证是发给当前 Agent 的，检查 payee_agents 配置

## 金额类错误

### AMOUNT_EXCEED_LIMIT
**含义：** 金额超过授权限额
**用户提示：** "请求金额超过了授权限制，请减少金额或重新申请更大的授权"
**处理：** 检查凭证中的 max_single_amount / max_total_amount 限制

### INSUFFICIENT_BALANCE
**含义：** 用户钱包余额不足
**用户提示：** "余额不足，请先充值"
**处理：** 引导用户充值后重试

## 支付类错误

### FREEZE_FAILED
**含义：** 冻结操作失败
**用户提示：** "资金冻结失败，请稍后重试"
**处理：** 检查余额是否充足，凭证是否仍然有效

### SETTLE_FAILED
**含义：** 结算操作失败
**用户提示：** "结算失败，请稍后重试"
**处理：** 检查是否已冻结、结算金额是否超过冻结金额

### PAYMENT_NOT_FOUND
**含义：** 找不到对应的支付交易
**用户提示：** "找不到对应的支付记录"
**处理：** 确认已先调用 lock_funds 冻结资金

## 托管模式错误

### CUSTODIAN_NOT_ALLOWED
**含义：** 不允许托管支付
**用户提示：** "当前不支持托管支付模式"
**处理：** 检查两个条件：
1. 调用方 Agent 是否为 PLATFORM 类型
2. 收款方 Agent 是否已将调用方设为托管操作方（custodian_agent_did）

## 通用处理原则

1. **不向用户暴露技术细节**（error_code、stack trace 等）
2. **用自然语言说明问题和解决建议**
3. **可重试的错误自动重试一次**（FREEZE_FAILED、SETTLE_FAILED）
4. **不可重试的错误立即告知用户**（INSUFFICIENT_BALANCE、MANDATE_EXPIRED）
5. **签约类错误引导签约**（QUOTA_NOT_FOUND → signing_guide.md）
