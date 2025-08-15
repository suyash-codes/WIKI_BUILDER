from flask import Flask, render_template_string, request, send_from_directory
import textwrap
import re
import os

from data_extractor import extract_wiki_content  # must return (full_text, page_url)

app = Flask(__name__, static_folder=".")

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Interactive Wikipedia Viewer</title>
  <style>
    body { font-family: Arial, sans-serif; background:#f5f6fa; margin:0; }
    header { background:#2f6fb1; color:white; padding:16px; text-align:center; }
    .container { max-width:1000px; margin:20px auto; background:white; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }
    form { display:flex; gap:8px; margin-bottom:16px; }
    input[type="text"]{ flex:1; padding:10px; font-size:16px; border:1px solid #ddd; }
    button{ padding:10px 14px; border:none; background:#2f6fb1; color:white; cursor:pointer }
    .meta { margin-bottom:12px; }
    .toc { background:#fafafa; border:1px solid #eee; padding:10px; margin-bottom:16px; }
    .toc a { color:#2f6fb1; text-decoration:none }
    h2.section-title { border-bottom:1px solid #eee; padding-bottom:6px; margin-top:28px; }
    p { text-align:justify; line-height:1.65; margin:10px 0; }
    .error { color: #9a1f1f; background: #fff1f1; padding:10px; border-radius:4px; margin-bottom:12px; }
    .actions { margin-top:14px; display:flex; gap:8px; }
    .download { text-decoration:none; color:#fff; background:#28a745; padding:8px 10px; border-radius:4px; }
    footer { text-align:center; font-size:13px; color:#666; margin-top:18px; }
  </style>
</head>
<body>
  <header><h1>📚 Interactive Wikipedia Viewer</h1></header>
  <div class="container">
    <form method="GET" action="/">
      <input type="text" name="topic" placeholder="Enter topic (e.g. ChatGPT, Python programming)" value="{{ topic|default('') }}">
      <button type="submit">Search</button>
    </form>

    {% if error %}
      <div class="error">{{ error }}</div>
    {% endif %}

    {% if title %}
      <div class="meta">
        <strong style="font-size:18px;">📚 {{ title }}</strong><br />
        🔗 Source: <a href="{{ link }}" target="_blank">{{ link }}</a>
      </div>

      <div class="actions">
        <a class="download" href="/download/{{ filename }}">⬇️ Download .txt</a>
      </div>

      <div class="toc">
        <strong>Table of contents</strong>
        <ol>
          {% for s in sections %}
            <li><a href="#{{ s.anchor }}">{{ s.title }}</a></li>
          {% endfor %}
        </ol>
      </div>

      {% for s in sections %}
        <h2 id="{{ s.anchor }}" class="section-title">{{ s.title }}</h2>
        {% for p in s.paragraphs %}
          <p>{{ p }}</p>
        {% endfor %}
      {% endfor %}

    {% else %}
      <p>Enter a topic above and press Search to fetch the full Wikipedia article and view it here.</p>
    {% endif %}

    <footer>Built with Python + Flask • File lines wrapped at 120 characters for .txt</footer>
  </div>
</body>
</html>
"""

def parse_wiki_text(full_text):
    """
    Convert plain extract (from the Wikipedia API) into a list of sections:
    [{'title': 'Introduction', 'anchor':'intro', 'paragraphs': [...]}, ...]
    Headings in the API extract are usually in the form of "\n== Heading ==\n".
    """
    if not full_text or not full_text.strip():
        return []

    text = full_text.replace('\r\n', '\n')

    # Regex to find headings like: '\n== Heading ==\n' or '=== Subheading ==='
    heading_re = re.compile(r'\n={2,}\s*(.+?)\s*={2,}\n')
    matches = list(heading_re.finditer(text))

    sections = []

    # If there are no explicit headings, treat entire text as Introduction
    if not matches:
        paras = [p.strip() for p in re.split(r'\n{2,}', text.strip()) if p.strip()]
        sections.append({
            'title': 'Introduction',
            'anchor': 'introduction',
            'paragraphs': paras
        })
        return sections

    # Intro (text before first heading)
    first = matches[0]
    intro_text = text[: first.start() ].strip()
    if intro_text:
        paras = [p.strip() for p in re.split(r'\n{2,}', intro_text) if p.strip()]
        sections.append({'title':'Introduction', 'anchor':'introduction', 'paragraphs': paras})

    # For each heading, extract content until next heading
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        section_text = text[start:end].strip()
        paras = [p.strip() for p in re.split(r'\n{2,}', section_text) if p.strip()]
        # create a safe anchor (lowercase, replace spaces & non-alnum)
        anchor = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        if not anchor:
            anchor = f"section-{i+1}"
        sections.append({'title': title, 'anchor': anchor, 'paragraphs': paras})

    return sections

@app.route("/", methods=["GET"])
def home():
    topic = request.args.get("topic", "").strip()
    title = None
    link = None
    sections = []
    filename = None
    error = None

    if topic:
        try:
            # Get full text and canonical wikipedia link
            full_text, page_url = extract_wiki_content(topic)

            if not full_text or not full_text.strip():
                raise ValueError("No extractable content returned for this topic.")

            title = page_url.rsplit("/", 1)[-1].replace('_', ' ')
            link = page_url
            sections = parse_wiki_text(full_text)

            # Save wrapped TXT file (120 chars per line, no blank lines)
            filename = f"{topic.replace(' ', '_')}.txt"
            header = f"📚 {title} 📚\n" + ("=" * (len(title) + 8)) + "\n"
            header += f"🔗 Source: {link}\n\n"

            wrapped = "\n".join(textwrap.wrap(full_text, width=120))
            with open(filename, "w", encoding="utf-8") as f:
                f.write(header + wrapped)

        except Exception as e:
            error = str(e)
            sections = []
            link = None
            filename = None

    return render_template_string(HTML_TEMPLATE,
                                  topic=topic,
                                  title=title,
                                  link=link,
                                  sections=sections,
                                  filename=filename,
                                  error=error)

@app.route("/download/<path:filename>")
def download(filename):
    # Serves the generated .txt file from current working directory
    safe_dir = os.getcwd()
    return send_from_directory(safe_dir, filename, as_attachment=True)

if __name__ == "__main__":
    # Run dev server
    app.run(debug=True, port=5000)
