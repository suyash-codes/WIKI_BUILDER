import textwrap

def format_wiki_page(title, summary, wiki_url):
    file_name = f"{title.replace(' ', '_')}.txt"
    wrapped_summary = "\n".join(textwrap.wrap(summary, width=120))

    heading = f"📚 WIKIPEDIA STYLE PAGE: {title.upper()} 📚"
    underline = "=" * len(heading)

    content = (
        f"{heading}\n{underline}\n\n"
        f"🔗 Wikipedia Source: {wiki_url}\n\n"
        f"{wrapped_summary}"
    )

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)

    print(content)  # Show in terminal
    print(f"\n✅ Wikipedia-style summary saved as {file_name}")
