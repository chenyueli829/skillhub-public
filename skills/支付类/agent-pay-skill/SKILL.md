---
name: cyl-agent-pay-skill
description: AI钱包支付助手。当用户需要开通AI钱包、付款购买服务、收款、查余额时使用。
metadata: {"openclaw": {"emoji": "💰", "requires": {"bins": ["python3", "bash"]}}}
---

# AI 钱包支付助手

## 约束

- 只运行本文档列出的脚本，不要推断或编造脚本名（不存在 login.py、bind.py 等）
- 不要读取 `{baseDir}/lib/keys/` 下的 `.pem` 文件
- 不要展示私钥、JWT Token 完整内容
- 所有支付必须基于 L3 签约关系，由系统强制校验额度

---

## 前置检查

每次操作前先运行：

```bash
bash {baseDir}/scripts/check_env.sh
```

| 输出包含 | 操作 |
|---------|------|
| `READY` | 按「场景路由」操作 |
| `PENDING_ACTIVATION` | 输出中包含 session_id，说明之前已创建注册会话等待验证码。如果用户本轮消息包含 6 位数字验证码，直接运行 `python3 {baseDir}/setup/finalize_setup.py --session-id <输出中的session_id> --token <验证码>`；否则提示用户提供验证码 |
| `DEPS_MISSING` | `pip3 install -r {baseDir}/requirements.txt`，然后重新检查 |
| `SIGNER_NOT_INITIALIZED` 或其他非 READY | 执行「首次接入」 |

---

## 场景路由

| 用户意图 | 操作 |
|---------|------|
| "开通钱包"、"接入支付" | 执行「首次接入」 |
| 调用外部服务后对方返回了报价或要求 `authorization_mandate` | 加载 [payment_guide.md]({baseDir}/references/payment_guide.md) |
| 用户主动说"付款"、"购买服务" | 加载 [payment_guide.md]({baseDir}/references/payment_guide.md) |
| 授权时返回 error_code=60001 (QUOTA_NOT_FOUND) | 加载 [signing_guide.md]({baseDir}/references/signing_guide.md)（服务签约流程） |
| 授权返回 confirm_status=PENDING_CONFIRM | 提示用户去小程序确认，用户回复已确认后执行 `python3 {baseDir}/scripts/query_mandate.py --mandate-id <凭证ID>` |
| "收款"、收到带 authorization_mandate 的入站请求 | 加载 [collection_guide.md]({baseDir}/references/collection_guide.md) |
| "查余额" | `python3 {baseDir}/setup/query_balance.py`，将余额（元）告知用户 |
| "签约服务"、"开通自动支付" | 加载 [signing_guide.md]({baseDir}/references/signing_guide.md) |
| 遇到错误（success: false） | 加载 [error_guide.md]({baseDir}/references/error_guide.md) |

---

## 首次接入

运行：

```bash
python3 {baseDir}/setup/register.py
```

然后严格按以下顺序操作：

1. **发送二维码图片**：先输出 `message_to_user` 的文案，然后使用 `MEDIA:` 协议发送图片（**不要用 Markdown 语法，不要用 message tool**）。格式：
   ```
   <message_to_user 的内容>

   MEDIA:<qr_image_path 的绝对路径>
   ```
2. 输出 `NO_REPLY` 结束本轮对话，不要追加任何文字
3. 用户回复 6 位验证码后，按 `next_action` 中的命令执行（会自动完成密钥生成、激活、配置、验证的全部流程）

> ⚠️ **严格禁止**：
> - 不要用 `![image](...)` Markdown 语法嵌入图片
> - 不要读取图片文件内容或转为 base64 / data URI
