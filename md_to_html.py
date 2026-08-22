import sys
import os
import markdown

def generate_html(md_file_path):
    if not os.path.exists(md_file_path):
        print(f"Error: File '{md_file_path}' not found.")
        sys.exit(1)

    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    md_parser = markdown.Markdown(extensions=['fenced_code', 'codehilite', 'tables', 'toc'])
    html_body = md_parser.convert(md_content)
    
    toc_html = getattr(md_parser, 'toc', '<ul><li><a href="#">Table of Contents</a></li></ul>')

    base_name = os.path.splitext(os.path.basename(md_file_path))[0]
    page_title = base_name.replace('_', ' ').title()

    html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <!-- GitHub Markdown CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/sindresorhus/github-markdown-css/github-markdown.css">
  <style>
    :root {{
      --bg: #0d1117;
      --fg: #c9d1d9;
      --muted: #8b949e;
      --border: #30363d;
      --accent: #58a6ff;
      --code-bg: #161b22;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--fg);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    /* Layout */
    .stackedit__left {{
      position: fixed;
      top: 0;
      left: 0;
      bottom: 0;
      width: 280px;
      overflow-y: auto;
      background: #010409;
      border-right: 1px solid var(--border);
      padding: 20px;
    }}
    .stackedit__right {{
      margin-left: 280px;
    }}
    /* TOC styling */
    .stackedit__toc a {{
      color: var(--fg);
      text-decoration: none;
      display: block;
      padding: 4px 6px;
      border-radius: 4px;
      margin-bottom: 4px;
    }}
    .stackedit__toc li:not(.toc-h3) a {{
      font-weight: 600;
      font-size: 14px;
    }}
    .stackedit__toc .toc-h3 a {{
      color: var(--muted);
      font-weight: 400;
      font-size: 13px;
      padding-left: 16px;
      border-left: 1px solid var(--border);
    }}
    .stackedit__toc a:hover {{
      color: var(--accent);
      background: rgba(88,166,255,0.15);
    }}
    .stackedit__toc a.active {{
      color: var(--accent);
      background: rgba(88,166,255,0.2);
    }}
    /* Markdown body */
    .markdown-body {{
      box-sizing: border-box;
      min-width: 200px;
      max-width: 980px;
      margin: 0 auto;
      padding: 45px;
      background: var(--bg);
      color: var(--fg);
    }}
    .markdown-body pre,
    .markdown-body code {{
      background: var(--code-bg);
    }}
    .markdown-body a {{ color: var(--accent); }}
    .markdown-body hr {{ border-color: var(--border); }}
    .markdown-body table th,
    .markdown-body table td {{ border-color: var(--border); }}
    @media (max-width: 900px) {{
      .stackedit__left {{
        position: relative;
        width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--border);
      }}
      .stackedit__right {{ margin-left: 0; }}
    }}
  </style>
</head>
<body>
  <div class="stackedit__left">
    <div class="stackedit__toc">
      {toc_html}
    </div>
  </div>
  <div class="stackedit__right">
    <div class="stackedit__html markdown-body">
      {html_body}
    </div>
  </div>
  <script>
    const tocLinks = document.querySelectorAll('.stackedit__toc a');
    tocLinks.forEach(a => {{
      const href = a.getAttribute('href');
      if (href?.startsWith('#')) {{
        a.addEventListener('click', e => {{
          e.preventDefault();
          tocLinks.forEach(link => link.classList.remove('active'));
          a.classList.add('active');
          const id = href.slice(1);
          const target = document.getElementById(id);
          if (target) {{
            const y = target.getBoundingClientRect().top + window.scrollY - 90;
            window.scrollTo({{ top: y, behavior: 'smooth' }});
          }}
        }});
      }}
    }});
  </script>
</body>
</html>
"""

    output_file = f"{base_name}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"Success! Generated '{output_file}' from '{md_file_path}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_html.py <your_file.md>")
        sys.exit(1)
    
    generate_html(sys.argv[1])
