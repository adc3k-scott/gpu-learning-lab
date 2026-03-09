"""
Build a fully self-contained shareable HTML from index.html.
- Embeds Google Fonts as base64 @font-face
- Embeds all external images as base64 data URIs
- Outputs MARLIE-I-Investor-Deck-SHARE.html
"""
import sys, re, base64, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\index.html"
OUT = r"c:\Users\adhsc\OneDrive\Documents\GitHub\gpu-learning-lab\marlie\MARLIE-I-Investor-Deck-SHARE.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), r.headers.get("Content-Type", "")

def url_to_data_uri(url):
    print(f"  Fetching: {url[:80]}")
    try:
        data, ct = fetch(url)
        ct = ct.split(";")[0].strip()
        if not ct or ct == "application/octet-stream":
            ext = url.split("?")[0].split(".")[-1].lower()
            ct = {"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png",
                  "gif":"image/gif","svg":"image/svg+xml","webp":"image/webp"}.get(ext,"image/jpeg")
        b64 = base64.b64encode(data).decode()
        return f"data:{ct};base64,{b64}"
    except Exception as e:
        print(f"  WARN: could not fetch {url[:60]}: {e}")
        return url

# ── Load source ──────────────────────────────────────────────────
with open(SRC, "r", encoding="utf-8") as f:
    html = f.read()

# ── Embed Google Fonts ───────────────────────────────────────────
gfonts_pat = re.compile(r'<link[^>]+fonts\.googleapis\.com[^>]+>')
gfonts_match = gfonts_pat.search(html)
font_css_block = ""
if gfonts_match:
    gfonts_url = re.search(r'href="([^"]+)"', gfonts_match.group()).group(1)
    print(f"Fetching Google Fonts CSS: {gfonts_url[:80]}")
    try:
        css_bytes, _ = fetch(gfonts_url)
        css_text = css_bytes.decode("utf-8")
        # Download each font file referenced in the CSS and embed
        font_url_pat = re.compile(r'url\((https://[^)]+)\)')
        def embed_font(m):
            fu = m.group(1)
            print(f"  Font: {fu[:80]}")
            try:
                fd, fct = fetch(fu)
                fct = fct.split(";")[0].strip() or "font/woff2"
                return f"url(data:{fct};base64,{base64.b64encode(fd).decode()})"
            except Exception as e:
                print(f"  WARN font: {e}")
                return m.group(0)
        css_text = font_url_pat.sub(embed_font, css_text)
        font_css_block = f"<style>\n{css_text}\n</style>"
        html = gfonts_pat.sub(font_css_block, html)
        print("Google Fonts embedded.")
    except Exception as e:
        print(f"WARN: could not fetch Google Fonts: {e}")

# ── Embed external images (src="https://...") ────────────────────
print("\nEmbedding external images...")
def embed_img_src(m):
    url = m.group(1)
    if url.startswith("data:"):
        return m.group(0)
    data_uri = url_to_data_uri(url)
    return f'src="{data_uri}"'

html = re.sub(r'src="(https?://[^"]+)"', embed_img_src, html)

# ── Write output ─────────────────────────────────────────────────
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

size_mb = len(html.encode("utf-8")) / 1_048_576
print(f"\nDone. Output: {OUT}")
print(f"File size: {size_mb:.1f} MB")
