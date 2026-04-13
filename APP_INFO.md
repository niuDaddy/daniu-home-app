# 大牛の家 APP 构建指南

## 技术栈
- 前端：纯 HTML/CSS/JS（`www/` 目录）
- 封装：Capacitor → Android APK
- 构建：GitHub Actions（`build-android.yml`）
- 产物：APK（`app-debug.apk`）

## 版本管理
- `android/` 目录不入库（gitignore），CI 每次 `npx cap add` 重新生成
- 版本号在 CI workflow 的 **Set version** 步骤注入：
  - `versionCode` — 整数，每次发布 +1（当前：31）
  - `versionName` — 显示用（当前：1.0.31）
- **改版本号只改 workflow 文件即可**

## 发布流程
1. 修改 `www/` 内容（页面、导航等）
2. 如果需要 APP 内打开新域名 → 更新 `capacitor.config.json` 的 `allowNavigation`
3. 更新 workflow 中 versionCode +1、versionName
4. git commit + push → 自动构建 APK

## 历史版本
| 版本 | versionCode | 改动 |
|------|-------------|------|
| 1.0.31 | 31 | 加小花身体记录（xiaohua.daniu.win）|

## 注意事项
- `scripts/patch-bridge.sh` 已移除 — Capacitor 7.x 的 `allowNavigation` 原生支持 WebView 内打开
- 首页（www/index.html）实际从 daniu.win 在线加载，APK 内的 index.html 是 fallback
