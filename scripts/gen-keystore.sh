#!/bin/bash
# Run locally once to generate a fixed keystore, then base64 it for GitHub secret
keytool -genkeypair -v \
  -keystore daniu-release.keystore \
  -alias daniu \
  -keyalg RSA -keysize 2048 \
  -validity 10000 \
  -storepass daniu2026 \
  -keypass daniu2026 \
  -dname "CN=Daniu, OU=Dev, O=DaniuHome, L=Shanghai, ST=Shanghai, C=CN"
base64 -i daniu-release.keystore | pbcopy
echo "✅ Base64 copied to clipboard — paste as GitHub secret KEYSTORE_BASE64"
echo "Also add secrets: KEYSTORE_PASSWORD=daniu2026 KEY_ALIAS=daniu"
