# Telegram Channel Summary 电报频道总结

> 使用 Telegram 开发者 API 快速汇总频道的关键数据，帮助你洞察频道动态。

## 项目简介

本工具基于 Python 与 Telethon，自动拉取 Telegram 频道的订阅数、消息内容等核心信息，并整理成易于阅读的总结。

## 快速开始

### 1. 安装依赖

确保已安装 Python，随后执行下列命令安装 Telethon：

```bash
pip install telethon
```

### 2. 配置开发者凭据

1. 访问 [Telegram 开发者页面](https://my.telegram.org/apps)。
2. 获取你的 `api_id` 与 `api_hash`。
3. 打开 `tg.py` 文件，将其中的 `api_id` 与 `api_hash` 替换为你的凭据。

### 3. 设置频道参数

- 在 `tg.py` 中的 `channel` 变量填写你要统计的频道用户名。
- 根据频道规模调整 `BATCH_SIZE`，若消息数量超过 1000 条建议适当增大以避免限速。

### 4. 运行脚本

执行以下命令启动脚本：

```bash
python tg.py
```

首次运行需按照提示输入绑定的手机号（包含国家区号，例如 `+13333333333`），随后在 Telegram 中收到验证码并输入即可。稍候片刻，脚本会输出频道总结。

## 输出示例

![Renderings](pic.png)

---

更多语言版本请见：

- [English README](README_EN.md)
- [Español README](README_ES.md)
