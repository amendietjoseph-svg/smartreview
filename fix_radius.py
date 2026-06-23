import glob

style = """<style>
div { border-radius: 16px !important; }
button { border-radius: 12px !important; }
input, select, textarea { border-radius: 10px !important; }
.navbar, .sidebar, body, html { border-radius: 0 !important; }
.avatar { border-radius: 50% !important; }
</style></head>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('</head>', style)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')