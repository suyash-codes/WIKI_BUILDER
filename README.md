📚 Personal Wikipedia Builder

An AI-powered tool that extracts complete Wikipedia articles, summarizes them, formats them in a clean, Wikipedia-style .txt file, and displays them interactively on a website — all using the Groq API for fast and intelligent summarization.

🚀 Features

Full Wikipedia Page Extraction – Uses the Wikipedia API to fetch the correct article and all its sections.

AI-Powered Summarization – Summarizes content with the Groq API while preserving important details.

TXT File Output – Saves output in .txt format with the Wikipedia link included.

Interactive Website View – Displays content with styled formatting for better reading.

Customizable Content Length – Adjustable to give you more or less detail.

🛠️ Tech Stack

Python 3.10+

Groq API (for summarization)

Wikipedia API (for accurate page fetching)

BeautifulSoup4 (for HTML parsing)

Flask (for website display)

📂 Project Structure
personal_wiki_builder/
│
├── app.py                  # Main application entry point
├── data_extractor.py       # Wikipedia content extraction
├── summarizer.py           # Groq API summarization logic
├── templates/
│   └── index.html          # Website UI
├── static/
│   └── style.css           # Website styles
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

⚙️ Installation & Setup

Clone the Repository

git clone https://github.com/yourusername/personal-wiki-builder.git
cd personal-wiki-builder


Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install Dependencies

pip install -r requirements.txt


Set Up Environment Variables
Create a .env file and add your Groq API key:

GROQ_API_KEY=your_api_key_here


Run the App

python app.py

📄 Usage

Enter the topic name when prompted.

The script will:

Find the correct Wikipedia page

Extract the full content

Summarize it with Groq

Save a .txt file with the Wikipedia link

Show the content in your browser with an interactive format

The .txt file will be saved in the project folder.

📷 Example Output

TXT File

📚 WIKIPEDIA STYLE PAGE: CHATGPT 📚
=================================

🔗 Wikipedia Source: https://en.wikipedia.org/wiki/ChatGPT

== Introduction ==
ChatGPT is a generative AI language model developed by OpenAI...


Website View

Large, readable fonts

Clean, sectioned formatting

Wikipedia-style headings

📌 Future Improvements

Adding dark mode for website

Option to export as PDF

Multi-language Wikipedia support

👤 Author

Suyash Singh Gusain
📧 [https://github.com/suyash-codes]
🔗 [www.linkedin.com/in/suyashsinghgusain] 
