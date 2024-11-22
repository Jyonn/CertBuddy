# CertBuddy

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/)

自动化 HTTPS 证书申请和更新工具

---

## 简介

**CertBuddy** 是一款用于自动化申请腾讯云免费证书并在七牛云上部署 HTTPS 的工具。由于近期免费证书的有效期从 12 个月缩短到了 3 个月，且部署在七牛云的证书无法自动续期，因此开发了此工具以简化流程。

**支持场景：**

- 使用腾讯云自动 DNS 验证的方式申请免费的三个月证书。
- 在七牛云上上传自有证书，并部署到对应的对象存储空间。

---

## 特性

- **全自动化流程**：从证书申请到部署，全程自动化，无需人工干预。
- **多域名支持**：可批量处理多个域名的证书申请和部署。
- **易于配置**：简单的配置文件，即可快速开始使用。
- **可扩展性**：代码结构清晰，方便二次开发和功能扩展。

---

## 安装

### 环境依赖

- Python 3.x
- 已注册的腾讯云和七牛云账户
- pip 包管理器

### 安装依赖库

在项目根目录下运行：

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 配置认证信息

在项目根目录下创建 `.auth` 文件，内容如下：

```ini
tencentcloud-secret-id = YOUR-TENCENTCLOUD-SECRET-ID
tencentcloud-secret-key = YOUR-TENCENTCLOUD-SECRET-KEY
qiniu-access-key = YOUR-QINIU-ACCESS-KEY
qiniu-secret-key = YOUR-QINIU-SECRET-KEY
```

- 腾讯云密钥：可在 [腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi) 获取。
- 密钥：可在 [七牛云密钥管理](https://portal.qiniu.com/user/key) 获取。

### 2. 配置域名列表

在项目根目录下创建 `.joblist` 文件，内容如下：

```text
uvw.abc.com
xyz.abc.com
```

- 每个域名占一行。
- 不需要包含 https:// 前缀。

### 3. 运行工具

执行以下命令：

```bash
python certbuddy.py
```

### 4. 设置定时任务

为了让证书自动续期，可以使用 `crontab` 或 `systemd` 的 `timer` 来定时运行 `certbuddy.py`。

**使用 crontab 示例：**

```bash
# 每80天执行一次
0 0 */80 * * /usr/bin/python /path/to/certbuddy.py >> /path/to/certbuddy.log 2>&1
```

## 常见问题

**Q: 证书申请失败怎么办？**
A: 请检查您的腾讯云 API 密钥是否正确，域名是否已在腾讯云进行备案，且 DNS 解析设置正确。

## 贡献指南

欢迎对 `**CertBuddy**` 做出贡献！您可以通过以下方式：
- 提交 Issue 报告 Bug 或提出新功能建议。
- 提交 Pull Request，帮助我们支持更多的云服务平台和证书颁发机构。

## 开源协议

**CertBuddy** 使用 [MIT](LICENSE) 开源协议。
