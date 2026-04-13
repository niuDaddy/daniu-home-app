# 大牛の家 APP 构建指南

## 技术栈
- 前端：纯 HTML/CJS/JS（`www/` 目录）
- 封装：Capacitor 7.x → Android APK
- 构建：GitHub Actions（`.github/workflows/build-android.yml`）
- Repo：`github.com/niuDaddy/daniu-home-app`
- `android/` 目录不入库，CI 每次 `npx cap add android` 重新生成

## 版本管理
版本号在 CI workflow 的 **Set version** 步骤用 sed 注入：
- `versionCode` — 整数，每次发布 +1（当前：31）
- `versionName` — 显示用（当前：1.0.31）

## 固定签名
GitHub Secrets 存有固定 keystore：
- `KEYSTORE_BASE64` — base64 编码的 keystore
- `KEYSTORE_PASSWORD` — 密码
- `KEY_ALIAS` — daniu

CI 构建后用 `apksigner sign` 重新签名，确保每次签名一致，可覆盖安装。

## 发布流程
1. 修改 `www/` 内容（页面、导航等）
2. 如果需要 APP 内打开新域名 → 更新 `capacitor.config.json` 的 `allowNavigation`
3. 更新 workflow 中 versionCode +1、versionName
4. git commit + push → 自动构建 APK
5. Actions 页面 → Artifacts → 下载 `daniu-home-apk`

## 历史版本
| 版本 | versionCode | 改动 |
|------|-------------|------|
| 1.0.31 | 31 | 加小花身体记录（xiaohua.daniu.win）|

## 关键注意事项
- **Bridge.java patch 必须保留** — 强制所有链接在 WebView 内打开，不能删
- **不要改成 `npm ci`** — `npm install` 才能正确安装
- **首页从 daniu.win 在线加载** — APK 内的 index.html 是 fallback
