#!/usr/bin/env python3
"""Inject refresh button + pull-to-refresh into all pages via BridgeWebViewClient.java"""
import re

CLIENT = 'node_modules/@capacitor/android/capacitor/src/main/java/com/getcapacitor/BridgeWebViewClient.java'

# JavaScript to inject (creates a floating refresh button + pull-to-refresh gesture)
JS = (
    '(function(){'
    'if(document.getElementById("__daniu_r"))return;'
    'var st=document.createElement("style");'
    'st.textContent="#__daniu_r{position:fixed;top:16px;right:16px;width:40px;height:40px;'
    'border:none;background:rgba(255,255,255,.9);backdrop-filter:blur(8px);border-radius:50%;'
    'font-size:1.2em;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.12);z-index:10000;'
    'display:flex;align-items:center;justify-content:center}";'
    'document.head.appendChild(st);'
    'var b=document.createElement("button");b.id="__daniu_r";b.textContent="\\u21BB";'
    'b.onclick=function(){location.reload()};'
    'document.body.appendChild(b);'
    'var sy=0,p=false;'
    'document.addEventListener("touchstart",function(e){'
    'if(window.scrollY===0){sy=e.touches[0].clientY;p=true}'
    '},{passive:true});'
    'document.addEventListener("touchmove",function(e){'
    'if(!p)return;if(e.touches[0].clientY-sy>80&&window.scrollY===0){p=false;location.reload()}'
    '},{passive:true});'
    'document.addEventListener("touchend",function(){p=false},{passive:true});'
    '})();'
)

with open(CLIENT, 'r') as f:
    content = f.read()

if '__daniu_r' in content:
    print('⚠️  Already patched, skipping')
    exit(0)

# Find onPageFinished and inject after super.onPageFinished and listener loop
# Pattern: find the closing brace of onPageFinished method
pattern = r'(@Override\s*\n\s*public void onPageFinished\(WebView view, String url\)\s*\{.*?\n\s*\})(?=\s*\n\s*@Override)'

match = re.search(pattern, content, re.DOTALL)
if match:
    # Inject our evaluateJavascript call at the end of onPageFinished
    method_body = match.group(1)
    # Insert before the closing brace
    inject = f'\n        // DANIU: inject refresh button for external pages\n        if (!url.startsWith("file:") && !url.startsWith("capacitor:") && !url.equals("about:blank")) {{\n            view.evaluateJavascript("{JS}", null);\n        }}\n    '
    new_body = method_body[:-1] + inject + '}'
    content = content[:match.start()] + new_body + content[match.end():]
    print('✅ Injected into onPageFinished')
else:
    print('❌ Could not find onPageFinished method')
    exit(1)

with open(CLIENT, 'w') as f:
    f.write(content)
print('✅ BridgeWebViewClient.java patched')
