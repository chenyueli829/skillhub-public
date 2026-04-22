# 服务签约指南

当用户首次使用某个付费服务，且 authorize.py 返回 error_code=60001 (QUOTA_NOT_FOUND) 时，需要先完成 L3 服务签约。

## 流程

### 1. 发起签约

```bash
python3 {baseDir}/scripts/sign_service.py --payee <收款方服务名>
```

或使用 DID：

```bash
python3 {baseDir}/scripts/sign_service.py --payee-did <收款方Agent DID>
```

### 2. 发送二维码

先输出 `message_to_user` 的文案，然后使用 `MEDIA:` 协议发送图片（**不要用 Markdown 语法，不要用 message tool**）。格式：
```
<message_to_user 的内容>

MEDIA:<qr_image_path 的绝对路径>
```

### 3. 等待用户完成签约

用户在小程序中完成以下设置：
- 单笔限额
- 每日/每月累计限额
- 确认模式（自动放行 或 笔笔确认）

### 4. 签约完成

用户回复"已签约"或类似确认后，**直接回到付款流程**（[payment_guide.md]({baseDir}/references/payment_guide.md) 第 2 步），重新执行 authorize.py。

> 💡 **无需额外验证**：签约完成后不需要运行任何 finalize 脚本，直接重新申请凭证即可。

## 注意事项

- 签约关系由用户在小程序端管理，agent_pay 只读
- 同一 payer-payee 组合只需签约一次，后续使用自动基于签约额度
- 用户可随时在小程序中修改签约额度或确认模式

> ⚠️ **严格禁止**：
> - 不要用 `![image](...)` Markdown 语法嵌入图片
> - 不要读取图片文件内容或转为 base64 / data URI
