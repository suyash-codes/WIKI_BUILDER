from data_extractor import extract_wiki_content
from summarizer import summarize_content
from page_formatter import format_wiki_page

def main():
    topic = input("Enter the topic: ").strip()
    print("🔍 Extracting data...")

    # Get Wikipedia content
    wiki_url, raw_data = extract_wiki_content(topic)

    print("✍ Summarizing content...")
    summary = summarize_content(raw_data)

    print("📄 Formatting Wikipedia-style page...")
    format_wiki_page(topic, summary, wiki_url)

    print("✅ Done! The file has been saved.")

if __name__ == "__main__":
    main()
