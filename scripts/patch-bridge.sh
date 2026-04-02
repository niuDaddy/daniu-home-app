#!/bin/bash
# Patch Capacitor Bridge.java to force all links to stay in WebView
# Usage: ./patch-bridge.sh

BRIDGE=$(find node_modules -path "*/capacitor/src/main/java/com/getcapacitor/Bridge.java" | head -1)

if [ -z "$BRIDGE" ]; then
    echo "Bridge.java not found"
    exit 1
fi

echo "Patching: $BRIDGE"

# Use perl for multi-line regex replacement
perl -i -0pe 's/public boolean launchIntent\(Uri url\) \{.*?return false;\s*\}/public boolean launchIntent(Uri url) {\n        \/\/ PATCHED: Force all links to stay in WebView\n        return false;\n    }/s' "$BRIDGE"

# Verify
if grep -q "PATCHED: Force all links" "$BRIDGE"; then
    echo "✅ Bridge.java patched successfully"
else
    echo "❌ Patch failed"
    exit 1
fi
