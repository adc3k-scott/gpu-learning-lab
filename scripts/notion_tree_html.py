"""
Mission Control — Render Notion workspace tree as HTML and open in browser.
Run: python scripts/notion_tree_html.py
"""
import sys, os, tempfile, webbrowser
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
from skills.builtin.notion_util import NotionClient, get_title

nc = NotionClient()
tree = nc.full_tree()
by_id = tree["by_id"]
children = tree["children"]
roots = tree["roots"]
total = len(by_id)

TYPE_COLORS = {
    "database": "#a78bfa",
    "page": "#60a5fa",
}
TYPE_ICONS = {
    "database": "DB",
    "page": "PG",
}

def render_node(oid, depth=0):
    obj = by_id.get(oid)
    if not obj:
        return ""
    ntype = obj.get("object", "page")
    title = get_title(obj)
    short_id = oid[:8]
    color = TYPE_COLORS.get(ntype, "#60a5fa")
    icon  = TYPE_ICONS.get(ntype, "PG")
    indent = depth * 24
    kids = children.get(oid, [])
    has_children = bool(kids)
    children_html = "".join(render_node(kid, depth + 1) for kid in kids)
    toggle = 'onclick="toggle(this)"' if has_children else ''
    cursor = "cursor:pointer;" if has_children else ""
    return f"""
    <div class="node" style="margin-left:{indent}px;">
      <div class="node-row" {toggle} style="{cursor}">
        <span class="badge" style="background:{color};">{icon}</span>
        <span class="title">{title}</span>
        <span class="nid">{short_id}</span>
        {'<span class="arrow open">▶</span>' if has_children else ''}
      </div>
      {'<div class="children">' + children_html + '</div>' if has_children else ''}
    </div>"""

body = "".join(render_node(r) for r in roots)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Notion Workspace Tree — Mission Control</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', monospace; font-size: 14px; padding: 24px; }}
  h1 {{ color: #34d399; font-size: 20px; margin-bottom: 4px; letter-spacing: 1px; }}
  .meta {{ color: #64748b; font-size: 12px; margin-bottom: 20px; }}
  .search-bar {{ margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
  #search {{ background: #1e293b; border: 1px solid #334155; color: #e2e8f0; padding: 8px 12px;
             border-radius: 6px; width: 360px; font-size: 14px; outline: none; }}
  #search:focus {{ border-color: #60a5fa; }}
  .node {{ margin: 2px 0; }}
  .node-row {{ display: flex; align-items: center; gap: 8px; padding: 5px 8px;
               border-radius: 6px; transition: background 0.15s; }}
  .node-row:hover {{ background: #1e293b; }}
  .badge {{ font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px;
            color: #0f172a; min-width: 28px; text-align: center; flex-shrink: 0; }}
  .title {{ flex: 1; color: #e2e8f0; }}
  .nid {{ color: #475569; font-size: 11px; font-family: monospace; }}
  .arrow {{ color: #94a3b8; font-size: 10px; transition: transform 0.2s; display: inline-block; }}
  .arrow.open {{ transform: rotate(90deg); }}
  .children {{ display: block; }}
  .children.collapsed {{ display: none; }}
  .highlight {{ background: #854d0e; border-radius: 3px; padding: 0 2px; }}
  .btn {{ background: #1e293b; border: 1px solid #334155; color: #94a3b8; padding: 6px 14px;
          border-radius: 6px; cursor: pointer; font-size: 12px; }}
  .btn:hover {{ background: #334155; color: #e2e8f0; }}
  #count {{ color: #64748b; font-size: 12px; }}
</style>
</head>
<body>
<h1>Notion Workspace Tree</h1>
<div class="meta">Total objects: {total} &nbsp;|&nbsp; Mission Control HQ</div>
<div class="search-bar">
  <input id="search" type="text" placeholder="Search pages..." oninput="filterTree(this.value)">
  <button class="btn" onclick="expandAll()">Expand All</button>
  <button class="btn" onclick="collapseAll()">Collapse All</button>
  <span id="count"></span>
</div>
<div id="tree">{body}</div>
<script>
function toggle(row) {{
  const arrow = row.querySelector('.arrow');
  const children = row.parentElement.querySelector('.children');
  if (!children) return;
  if (children.classList.contains('collapsed')) {{
    children.classList.remove('collapsed');
    if (arrow) arrow.classList.add('open');
  }} else {{
    children.classList.add('collapsed');
    if (arrow) arrow.classList.remove('open');
  }}
}}
function expandAll() {{
  document.querySelectorAll('.children').forEach(el => el.classList.remove('collapsed'));
  document.querySelectorAll('.arrow').forEach(el => el.classList.add('open'));
}}
function collapseAll() {{
  document.querySelectorAll('.children').forEach(el => el.classList.add('collapsed'));
  document.querySelectorAll('.arrow').forEach(el => el.classList.remove('open'));
}}
function filterTree(q) {{
  q = q.toLowerCase().trim();
  const count = document.getElementById('count');
  if (!q) {{
    document.querySelectorAll('.node').forEach(n => n.style.display = '');
    document.querySelectorAll('.title').forEach(el => el.innerHTML = el.textContent);
    count.textContent = '';
    return;
  }}
  let visible = 0;
  document.querySelectorAll('.node').forEach(node => {{
    const titleEl = node.querySelector(':scope > .node-row .title');
    if (!titleEl) return;
    const text = titleEl.textContent.toLowerCase();
    if (text.includes(q)) {{
      node.style.display = '';
      titleEl.innerHTML = titleEl.textContent.replace(new RegExp(q.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&'), 'gi'),
        m => '<span class="highlight">'+m+'</span>');
      visible++;
    }} else {{
      node.style.display = 'none';
    }}
  }});
  count.textContent = visible + ' matches';
  expandAll();
}}
</script>
</body>
</html>"""

tmp = os.path.join(tempfile.gettempdir(), "notion_tree.html")
with open(tmp, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Opened: {tmp}  ({total} objects)")
webbrowser.open(f"file:///{tmp.replace(chr(92), '/')}")
