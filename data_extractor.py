import requests

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

def extract_wiki_content(topic):
    """
    Searches Wikipedia for the topic and returns:
    - Clean full text of the page
    - Wikipedia link
    """

    # Step 1: Search for the best matching page
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": topic,
        "format": "json"
    }
    search_response = requests.get(WIKI_API_URL, params=search_params)
    search_data = search_response.json()

    if not search_data["query"]["search"]:
        raise ValueError(f"No Wikipedia page found for '{topic}'.")

    # Best match
    page_title = search_data["query"]["search"][0]["title"]
    page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"

    # Step 2: Get the page content (intro + all sections)
    content_params = {
        "action": "query",
        "prop": "extracts",
        "titles": page_title,
        "explaintext": True,   # plain text, no HTML
        "format": "json"
    }
    content_response = requests.get(WIKI_API_URL, params=content_params)
    content_data = content_response.json()

    page = next(iter(content_data["query"]["pages"].values()))
    full_text = page.get("extract", "")

    if not full_text.strip():
        raise ValueError(f"No extractable content found for '{page_title}'.")

    return full_text, page_url
