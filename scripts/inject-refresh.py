#!/usr/bin/env python3
"""Inject refresh button + pull-to-refresh into all pages via BridgeWebViewClient.java
Uses a temp file for the JS to avoid escaping issues."""
import re, os, tempfile

CLIENT = 'node_modules/@capacitor/android/capacitor/src/main/java/com/getcapacitor/BridgeWebViewClient.java'

with open(CLIENT, 'r') as f:
    content = f.read()

if '__daniu_r' in content:
    print('⚠️  Already patched, skipping')
    exit(0)

# The JS code we want to inject as a Java string literal
# We write it as a raw string, then properly escape for Java
JS_RAW = """(function(){
if(document.getElementById("__daniu_r"))return;
var st=document.createElement("style");
st.textContent="#__daniu_r{position:fixed;top:16px;right:16px;width:40px;height:40px;border:none;background:rgba(255,255,255,.9);backdrop-filter:blur(8px);border-radius:50%;font-size:1.2em;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.12);z-index:10000;display:flex;align-items:center;justify-content:center}";
document.head.appendChild(st);
var b=document.createElement("button");
b.id="__daniu_r";
b.textContent="\\u21BB";
b.onclick=function(){location.reload()};
document.body.appendChild(b);
var sy=0,p=false;
document.addEventListener("touchstart",function(e){if(window.scrollY===0){sy=e.touches[0].clientY;p=true}},{passive:true});
document.addEventListener("touchmove",function(e){if(!p)return;if(e.touches[0].clientY-sy>80&&window.scrollY===0){p=false;location.reload()}},{passive:true});
document.addEventListener("touchend",function(){p=false},{passive:true});
})();"""

# Escape for Java string: backslash -> double backslash, quote -> escaped quote
JS_JAVA = JS_RAW.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

# Find onPageFinished method and inject at the end
pattern = (
    r'(@Override\s*\n'
    r'\s*public void onPageFinished\(WebView view, String url\)\s*\{'
    r'.*?\n'
    r'\s*\})'
    r'(?=\s*\n\s*@Override)'
)

match = re.search(pattern, content, re.DOTALL)
if not match:
    print('❌ Could not find onPageFinished method')
    exit(1)

# Build the injection code
inject_lines = [
    '',
    '        // DANIU: inject refresh button for external pages',
    '        if (!url.startsWith("file:") && !url.startsWith("capacitor:") && !url.equals("about:blank")) {',
    f'            view.evaluateJavascript("{JS_JAVA}", null);',
    '        }',
]

method_end = match.group(1)
# Insert before the closing brace of the method
lines = method_end.split('\n')
# Find the last line (closing brace)
closing_idx = len(lines) - 1
while closing_idx >= 0 and not lines[closing_idx].strip():
    closing_idx -= 1

# Insert our code before the closing brace
new_lines = lines[:closing_idx] + inject_lines + [lines[closing_idx]]
new_method = '\n'.join(new_lines)

content = content[:match.start()] + new_method + content[match.end():]

with open(CLIENT, 'w') as f:
    f.write(content)

print('✅ BridgeWebViewClient.java patched with refresh injection')
